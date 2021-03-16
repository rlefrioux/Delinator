import numpy as np
from osgeo import gdal
from osgeo import osr
from matplotlib import pyplot as plt 
import scipy
from scipy import stats
import statsmodels.api as sm 
import math
import pandas as pd
import seaborn as sns 

"""
def Gaussian_Kernel_Filter(input_mat):
    ravel_mat = input_mat.ravel()
    ravel_mat = ravel_mat[ravel_mat != -999]
    opti_bandwidth = sm.nonparametric.KDEMultivariate(ravel_mat, var_type='u').bw
    mat = np.where(input_mat==-999, 0, input_mat)
    final_arr = scipy.ndimage.gaussian_filter(input_mat, opti_bandwidth[0])
    final_arr = np.where(input_mat==-999, -999, final_arr)
    return final_arr
"""

"""
def Gaussian_Kernel(input_mat):
    kernel_mat = input_mat.ravel()
    kernel_mat = kernel_mat[kernel_mat != -999]
    opti_bandwidth = sm.nonparametric.KDEMultivariate(kernel_mat, var_type='u')
    kernel_vector = sm.nonparametric.KDEMultivariate.cdf(opti_bandwidth)
    print(kernel_vector)
"""


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

"""
def gaussian_kernel_matrix(bandwidth, x_size, y_size):
    mat_weight = np.zeros((x_size, y_size))
    x_center = int(x_size/2)
    y_center = int(y_size/2)
    for x in range(0, x_size, 1):
        for y in range(0, y_size, 1):
            mat_weight[x,y] = math.exp((-1/2)*(euclidean_dist(x_center, y_center, x, y)/bandwidth)**2)
    mat_weight[x_center, y_center] = 0
    return mat_weight
"""    

#Notice that the bandwidth should be an odd integer
def smooth_matrix(input_mat, bandwidth):
    arr = np.where(input_mat == -999, 0, input_mat)
    #Matrix smoothing    
    mat_weight = bisquare_kernel_matrix(bandwidth)
    final_arr = scipy.ndimage.convolve(arr, mat_weight)
    final_arr = final_arr / mat_weight.sum()
    final_arr = np.where(input_mat == -999, -999, final_arr)
    return final_arr




"""
#1. OPEN THE TIFF FILE
tiff_file = gdal.Open("D:/population/countries_2000/population_europe_2000_modified.tif")

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

final_arr = smooth_matrix(arr_img, 11)
print(final_arr)


histo_list = np.ravel(arr_img)
histo_list = histo_list[histo_list != -999]

#Create a graph of the none smooth density
sns.displot(x=histo_list, kind="kde")
plt.savefig("D:/test/none_smooth_population_density")
plt.close()

histo_list_smooth = np.ravel(final_arr)
histo_list_smooth = histo_list[histo_list != -999]

#Create a graph of the none smooth density
sns.displot(x=histo_list, kind="kde")
plt.savefig("D:/test/smooth_population_gaussian_density")
plt.close()

#Create graphs of CDFs
sns.displot(x=histo_list_smooth, kind="ecdf")
plt.savefig("D:/test/smooth_population_gaussian_CDFs")
plt.close()

sns.displot(x=histo_list, kind="ecdf")
plt.savefig("D:/test/none_smooth_population_CDFs")
plt.close()

#5.CREATE THE NEW TIFF FILE AND EXPORT IT

driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/smooth_population_bw11.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_arr)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file
"""