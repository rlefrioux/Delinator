from PIL import Image
import numpy as np
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import sys
from zipfile import ZipFile as zf
import copy
import pandas as pd
import time
import concurrent.futures
sys.path.insert(0, "D:/python_script/")
import cluster_maker as cm
import smooth_density as sd
import gaussian_smoothing as gs

def counterfactual_distrib(final_arr, kernel_matrix, ravel_arr, ysize, xsize):
    mat = np.random.choice(ravel_arr, (ysize, xsize))
    mat = np.where(final_arr == 0, mat, 0)
    smooth_mat = sd.smooth_matrix(mat, kernel_matrix=kernel_matrix)
    smooth_mat = np.where(final_arr == 1, -999, smooth_mat)
    ravel_mat = np.ravel(smooth_mat)
    ravel_mat = ravel_mat[ravel_mat != -999]
    return np.unique(ravel_mat, return_counts = True)

def delineator(input_tiff, output_tiff, perc):
    #1. OPEN THE TIFF FILE
    tiff_file = gdal.Open(input_tiff)

    #2. GET INFORMATION FROM THE TIFF FILE

    geotransform = tiff_file.GetGeoTransform()
    projection = tiff_file.GetProjection()
    band = tiff_file.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    #3. LOAD THE TIFF FILE IN AN ARRAY

    arr_img = tiff_file.ReadAsArray()
    arr_img = arr_img.astype(np.int)
    tiff_file = None #close it
    band = None #close it

    ############################
    ##4.OPERATION ON THE ARRAY##
    ############################



    #DELINEATION
    start = time.time()

    final_arr = np.where(arr_img==-999, 0, arr_img)
    final_arr = sd.smooth_matrix(input_mat=final_arr, bandwidth=2.2)
      
    
    final_arr = np.where(final_arr < perc, -2, final_arr)
    final_arr = np.where(final_arr > 0, 0, final_arr)
    final_arr = np.where(final_arr != 0, 1, final_arr)

    end = time.time()
    duration = end-start
    print("I finish the 1st delineation in "+str(duration)+" seconds")

    #CLEAN NONE CONTIGUOUS PIXELS

    start = time.time()

    for y, x in zip(*np.where(final_arr == 0)):
        pix = final_arr[y,x]
        c = 0
        if y-1>=0:
            c += final_arr[y-1,x] == pix
        if y+1<ysize:
            c += final_arr[y+1,x] == pix
        if x-1>=0:
            c += final_arr[y,x-1] == pix
        if x+1<xsize:
            c += final_arr[y,x+1] == pix
        if c == 0:
            final_arr[y,x] = 1

    end = time.time()
    duration = end-start
    print("I finish the cleaning of the none contiguous pixels in "+str(duration)+" seconds")


        #SECOND DELINEATION
    start = time.time()
    
     #####
    #tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000_modified.tif")
    #arr_img = tiff_file.ReadAsArray()
    #arr_img = arr_img.astype(np.int)
     ####
    
    kernel_matrix = sd.bisquare_kernel_matrix(bandwidth=2.2)
    array = np.where(final_arr == 0, arr_img, -1)
    ravel_arr = np.ravel(array)
    ravel_arr = ravel_arr[ravel_arr != -1]

    
    kwargs = {"final_arr" : final_arr,
              "ravel_arr" : ravel_arr,
              "kernel_matrix" : kernel_matrix,
              "ysize" : ysize,
              "xsize" : xsize}
    
    start = time.time()
    nb_iterations = 200
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        fut = []
        value_dict = {}
        for i in range(nb_iterations):
            fut.append(executor.submit(counterfactual_distrib, **kwargs))
            
        done = False
        while not done:
            for i, f in enumerate(fut):
                f_is_done = f.done()
                f_error = f.exception()
                if f_error:
                    raise f_error
                if f_is_done:
                    print(f"Iteration remaining {len(fut)-1} / {nb_iterations}")
                    fut.pop(i)
                    values, values_count = f.result()
                    for v, count in zip(values, values_count):
                        if v in value_dict.keys():
                            value_dict[int(v)] += int(count)
                        else:
                            value_dict[int(v)] = int(count)
            done = len(fut) == 0
    end = time.time()
    duration = end - start
    print("I finish the whole process in "+str(duration))
    print("Which make an average iterations time of "+str(duration/nb_iterations))
    
    num_count = 0
    keys = []
    values = []
    for k, v in value_dict.items():
        keys.append(int(k))
        values.append(v)
    
    df = pd.DataFrame({"keys": keys, "values": values})
    df = df.sort_values("keys")    
    total_count = df["values"].sum()
    
    for _, row in df.iterrows():
        key = row["keys"]
        value = row["values"]  
        if (num_count/total_count)*100 <= 99:
            num_count += value
        else:
            perc = key
            print("The 2nd percentile is : "+str(perc))
            break
        
    
    mask_arr = np.where(final_arr == 0, arr_img, 0)    
    mask_arr = sd.smooth_matrix(mask_arr, kernel_matrix=kernel_matrix)
    mask_arr = np.where(mask_arr <= perc, -1, mask_arr)
    mask_arr = np.where(mask_arr > 0, 0, mask_arr)
    mask_arr = np.where(mask_arr != 0, 1, mask_arr)


    end = time.time()
    duration = end-start
    print("I finish the 2nd delineation in "+str(duration)+" seconds")
    
    start = time.time()

    for y, x in zip(*np.where(mask_arr == 0)):
        pix = mask_arr[y,x]
        c = 0
        if y-1>=0:
            c += mask_arr[y-1,x] == pix
        if y+1<ysize:
            c += mask_arr[y+1,x] == pix
        if x-1>=0:
            c += mask_arr[y,x-1] == pix
        if x+1<xsize:
            c += mask_arr[y,x+1] == pix
        if c == 0:
            mask_arr[y,x] = 1

    end = time.time()
    duration = end-start
    print("I finish the cleaning of the none contiguous pixels in "+str(duration)+" seconds")


        #IDENTIFICATION OF THE "HIGHLY" POPULATED CLUSTERS


    start = time.time()

    cluster_list = cm.get_all_urban_cluster(final_arr)

    valid_clusters = []
    indexes = set((y, x) for y,x in zip(*np.where(mask_arr == 0)))
    for c in cluster_list:
        if len(indexes.intersection(c)) > 0:
            valid_clusters.append(c)


    end = time.time()
    duration = end-start
    print("I finish the identification of clusters in "+str(duration)+" seconds")


        #DELETE THE CLUSTER THAT ARE NOT "HIGHLY" POPULATED

    start = time.time()

    tmp_arr = np.ones(final_arr.shape)
    for c in valid_clusters:
        for y, x in c:
            tmp_arr[y,x] = 0

    final_arr = tmp_arr


    end = time.time()
    duration = end-start
    print("I finish the cleaning of not highly populated clusters in "+str(duration)+" seconds")


    #ADD SUBCENTERS
    
    final_arr = np.where(mask_arr==0, -1, final_arr)

    #5.CREATE THE NEW TIFF FILE AND EXPORT IT

    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk
    new_tiff = None #closes the file

if __name__ == "__main__":
    delineator("D:/population/countries_2019/population_europe_2019_modified.tif", "D:/test/europe_2019/population_europe_2019_p99_p99.tif", perc=419)
