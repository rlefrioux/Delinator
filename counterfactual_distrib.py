import numpy as np
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import sys
import scipy
import time
import seaborn as sns
sys.path.insert(0, "D:/python_script/")
import smooth_density as sd
import concurrent.futures



#1. OPEN THE TIFF FILE
tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000.tif")

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

ravel_arr_img = np.ravel(arr_img)
ravel_arr_img = ravel_arr_img[ravel_arr_img != -999]
img = None
kernel_matrix = sd.bisquare_kernel_matrix(bandwidth=1.8)
counter_distrib = np.empty((0), dtype = int)
mask_img = gdal.Open("D:/none_urban/countries/none_urban_europe.tif")
mask_arr = mask_img.ReadAsArray()
mask_arr = mask_arr.astype(np.bool_)
mask_img = None
value_dict= {}

 
def counterfactual_distrib(mask_arr = mask_arr, ravel_arr_img=ravel_arr_img, kernel_matrix=kernel_matrix, ysize=ysize, xsize=xsize):
    start = time.time()
    mat = np.random.choice(ravel_arr_img, (ysize, xsize))
    mat = np.where(mask_arr == True, 0, mat)
    mat = np.where(arr_img==-999, 0, mat)
    smooth_mat = sd.smooth_matrix(mat, kernel_matrix=kernel_matrix)
    smooth_mat = np.where(arr_img==-999, -999, smooth_mat)    
    ravel_mat = np.ravel(smooth_mat)
    ravel_mat = ravel_mat[ravel_mat != -999]
    return np.unique(ravel_mat, return_counts = True)

def main():
    kwargs = {"mask_arr" : mask_arr,
              "ravel_arr_img" : ravel_arr_img,
              "kernel_matrix" : kernel_matrix,
              "ysize" : ysize,
              "xsize" : xsize}
    start = time.time()
    nb_iterations = 10000
    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        fut = []
        global_value_dict = {}
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
                            value_dict[v] += count
                        else:
                            value_dict[v] = count
            done = len(fut) == 0
    end = time.time()
    duration = end - start
    print("I finish the whole process in "+str(duration))
    print("Which make an average iterations time of "+str(duration/nb_iterations))
    return value_dict

if __name__ == "__main__":
    value_dict = main()
    total_count = 0
    num_count = 0
    for key in value_dict:
        total_count += value_dict[key]
    for key in value_dict:
        if num_count/total_count*100 <= 95:
            num_count += value_dict[key]
        else:
            print(key)
            break

# Ecriture
import json
with open("D:/test/built_counterfactual_dict.json"):
    f.write(json.dumps(value_dict, indent=4))


# Lecture
with open("D:/test/built_counterfactual_dict.json"):
    content = f.read()
    value_dict = json.loads(content)