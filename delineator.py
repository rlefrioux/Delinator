from PIL import Image
import numpy as np
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import sys
from zipfile import ZipFile as zf
import time
sys.path.insert(0, "D:/python_script/")
import cluster_maker as cm

    
def delineator(input_tiff, output_tiff, percentile):
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
    tiff_file = None #close it
    band = None #close it

    ############################
    ##4.OPERATION ON THE ARRAY##
    ############################
    
   

    #DELINEATION
    start = time.time()
    
    perc = np.percentile(np.select(arr_img>0, arr_img) , percentile, interpolation = 'nearest')
    final_arr = np.where(arr_img <= perc, -2, arr_img)
    final_arr = np.where(final_arr >= 0, 0, final_arr) 
    final_arr = np.where(final_arr == -2, 1, final_arr)

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

    
    #CLIP THE SLAYER USING THE MASK ARRAY
    
    mask_arr = - np.ones((ysize, xsize))
    for y, x in zip(*np.where(final_arr == 0)):
        mask_arr[y,x] = arr_img[y,x]

    
    end = time.time()
    duration = end-start
    print("I finish the cleaning of the none contiguous pixels in "+str(duration)+" seconds")

    
        #REDELINEATION 
    start = time.time()
    
    perc = np.percentile(np.select(mask_arr>0, mask_arr) , percentile, interpolation = 'nearest')
    mask_arr = np.where(mask_arr <= perc, -1, mask_arr)
    mask_arr = np.where(mask_arr >= 0, 0, mask_arr) 
    mask_arr = np.where(mask_arr != 0, 1, mask_arr)
    
    end = time.time()
    duration = end-start
    print("I finish the 2nd delineation in "+str(duration)+" seconds")
    
        #IDENTIFICATION OF THE "HIGHLY" POPULATED CLUSTERS
    
    start = time.time()
    
    cluster_list = cm.get_all_urban_cluster(final_arr)
    valid_clusters = []
    mask_arr_indexes = set((y, x) for y,x in zip(*np.where(mask_arr == 0)))
    for c in cluster_list:
        if len(mask_arr_indexes.intersection(c)) > 0:
            valid_clusters.append(c)
    
    end = time.time()
    duration = end-start
    print("I finish the identification of clusters in "+str(duration)+" seconds")
    
        #DELETE THE CLUSTER THAT ARE NOT "HIGHLY" POPULATED
    
    start = time.time()    
    
    flattened_valid_clusters = set()
    for c in valid_clusters:
        flattened_valid_clusters = flattened_valid_clusters.union(c)
        
    
    mask = np.zeros(final_arr.shape, dtype=bool)
    for y, x in flattened_valid_clusters:
        mask[y, x] = True
    final_arr[~mask] = 1
    
    """
    for x in range(0 , xsize, 1):
        for y in range(0, ysize, 1):
            if (y, x) not in flattened_valid_clusters:
                final_arr[y,x] = 1
    """
    
    end = time.time()
    duration = end-start
    print("I finish the cleaning of not highly populated clusters in "+str(duration)+" seconds")
    
    
        #5.CREATE THE NEW TIFF FILE AND EXPORT IT
    
    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file

continents = ["europe", "africa", "north_america", "asia", "oceanie", "south_america"]

for c in continents:
    start = time.time()
    delineator("D:/population/countries_2000/population_"+c+"_2000.tif", "D:/test/p95_population_"+c+"_2000.tif", 95)
    end = time.time()
    duration = end-start
    print("I made it for "+c+" in "+str(duration)+" seconds")
    
    
    
    