import numpy as np
from osgeo import gdal
from osgeo import osr
from matplotlib import pyplot as plt 
import scipy
from scipy import stats
import statsmodels as sm 
import math
import pandas as pd
import seaborn as sns 
   
def euclidean_dist(x_1 , y_1, x_2, y_2):
    value = math.sqrt(((x_1-x_2)**2)+((y_1-y_2)**2))
    return value

def bisquare_kernel_matrix(bandwidth):
    mat_weight = np.zeros((bandwidth, bandwidth))
    x_center = int(bandwidth/2)
    y_center = int(bandwidth/2)
    for x in range(0, bandwidth, 1):
        for y in range(0, bandwidth, 1):
            mat_weight[x,y] = (1-(euclidean_dist(x_center, y_center, x, y)/bandwidth)**2)**2
    mat_weight[x_center, y_center] = 0
    return mat_weight

def smooth_matrix(input_mat):
    arr = np.where(input_mat == -999, 0, input_mat)
    #Rule of thumb
    #Scott's rule
    std = arr.std()
    nb_obs = np.count_nonzero(arr)
    diag = np.diagonal(arr)
    len_diag = len(diag)
    opti_bandwidth = std*((4/((len_diag+2)*nb_obs))**(1/(len_diag+4)))
    if (int(opti_bandwidth) % 2) == 0:
        opti_bandwidth = int(opti_bandwidth)+1
    else:
        opti_bandwidth = int(opti_bandwidth)
    #Matrix smoothing    
    mat_weight = bisquare_kernel_matrix(opti_bandwidth)
    final_arr = scipy.ndimage.convolve(arr, mat_weight)
    final_arr = final_arr / mat_weight.sum()
    final_arr = np.where(arr_img == -999, -999, final_arr)
    return final_arr
    

#1. OPEN THE TIFF FILE
tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000_modified.tif")

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

final_arr = smooth_matrix(arr_img)

histo_list = np.ravel(arr_img)
histo_list = histo_list[histo_list != -999]

#Create a graph of the none smooth density
sns.displot(x=histo_list, kind="kde")
plt.savefig("D:/test/none_smooth_built_density")
plt.close()

histo_list_smooth = np.ravel(final_arr)
histo_list_smooth = histo_list[histo_list != -999]

#Create a graph of the none smooth density
sns.displot(x=histo_list, kind="kde")
plt.savefig("D:/test/smooth_built_density")
plt.close()

#Create graphs of CDFs
sns.displot(x=histo_list_smooth, kind="ecdf")
plt.savefig("D:/test/smooth_built_CDFs")
plt.close()

sns.displot(x=histo_list, kind="ecdf")
plt.savefig("D:/test/none_smooth_built_CDFs")
plt.close()


#5.CREATE THE NEW TIFF FILE AND EXPORT IT

driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/smooth_built_opti.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_arr)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file

