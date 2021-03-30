import numpy as np
from osgeo import gdal
from osgeo import osr
from matplotlib import pyplot as plt 
import scipy
from scipy import stats
import statsmodels.api as sm
import statistics 
import math
import pandas as pd
import seaborn as sns 
import random
from statistics import mean
import time



def euclidean_dist(x_1 , y_1, x_2, y_2):
    value = math.sqrt(((x_1-x_2)**2)+((y_1-y_2)**2))
    return value

def bisquare_kernel_matrix(bandwidth):
    #Create a square matrix that have always an odd number of dimension
    if (int(bandwidth)*2 + 1 % 2) == 0:
        mat_size = int(bandwidth)*2 + 2
        mat_weight = np.zeros((mat_size, mat_size))
        x_center = int(mat_size/2)
        y_center = int(mat_size/2)
        for x in range(0, mat_size, 1):
            for y in range(0, mat_size, 1):
                if euclidean_dist(x_center, y_center, x, y)<=bandwidth: 
                    mat_weight[x,y] = (1-(euclidean_dist(x_center, y_center, x, y)/bandwidth)**2)**2        
                else:
                    mat_weight[x,y] = 0 
    else:
        mat_size = int(bandwidth)*2 + 1 
        mat_weight = np.zeros((mat_size, mat_size))
        x_center = int(mat_size/2)
        y_center = int(mat_size/2)
        for x in range(0, mat_size, 1):
            for y in range(0, mat_size, 1):
                if euclidean_dist(x_center, y_center, x, y)<=bandwidth:
                    mat_weight[x,y] = (1-(euclidean_dist(x_center, y_center, x, y)/bandwidth)**2)**2
                else:
                    mat_weight[x_center, y_center] = 0
    mat_weight[x_center, y_center] = 0
    return mat_weight
    


#Notice that the bandwidth should be an odd integer
def smooth_matrix(input_mat, bandwidth):
    arr = np.where(input_mat == -999, 0, input_mat)
    #Matrix smoothing    
    mat_weight = bisquare_kernel_matrix(bandwidth)
    final_arr = scipy.ndimage.convolve(arr, mat_weight)
    final_arr = final_arr / mat_weight.sum()
    final_arr = np.where(input_mat == -999, -999, final_arr)
    final_arr = np.around(final_arr, 0)
    return final_arr


def correlation_coefficient(mat_1, mat_2):
    numerator = np.mean((mat_1 - mat_1.mean()) * (mat_2 - mat_2.mean()))
    denominator = mat_1.std() * mat_2.std()
    if denominator == 0:
        return 0
    else:
        result = numerator / denominator
        return result

def pseudo_R_squared(input_mat, bandwidth, x_excluded, y_excluded): 
    excluded_mat = np.copy(input_mat)
    excluded_mat[x_excluded, y_excluded] = 0
    excluded_smooth_mat = smooth_matrix(input_mat=excluded_mat, bandwidth=bandwidth)
    corr = correlation_coefficient(mat_1=excluded_smooth_mat, mat_2=input_mat)
    pseudo_R_squared = corr**2
    return pseudo_R_squared



def avg_R_squared(input_mat, bandwidth, x_size, y_size):
    R_squared_list = []
    weight_list = []
    for x in range(0, x_size, 1):
        for y in range(0, y_size, 1):
            if input_mat[x,y] != 0:
                R_squared_list.append(pseudo_R_squared(input_mat=input_mat, bandwidth=bandwidth, x_excluded=x, y_excluded=y))
                weight_list.append(input_mat[x,y])
            else:
                R_squared_list.append(1)
                weight_list.append(input_mat[x,y])
    weight_sum = sum(weight_list)
    weight_list = weight_list/weight_sum
    avg_R_squared = mean(R_squared_list)
    return avg_R_squared


def Find_opti_bandwidth(input_mat, bw_lower, bw_upper, bw_jump):
    start = time.time()
    x_size = len(input_mat)
    y_size = len(input_mat[0])
    bandwidth = []
    R_squared_list = []
    for bw in np.arange(bw_lower, bw_upper, bw_jump):
        R_squared_list.append(avg_R_squared(input_mat=input_mat, bandwidth=bw, x_size=x_size, y_size=y_size))
        bandwidth.append(bw)
        max_R_squared = max(R_squared_list)
    max_index = R_squared_list.index(max_R_squared)
    opti_bw = bandwidth[max_index]
    end = time.time()
    duration = end-start
    print("I find the optimal bandwidth in "+str(duration)+" seconds" )
    return [opti_bw, max_R_squared]  



def random_mat_opti_bandwidths(nb_iterations, x_size, y_size, bw_lower, bw_upper, bw_jump):
    opti_bandwidths = []
    opti_R_squared = []
    iteration = 0
    start = time.time()
    tiff_file = gdal.Open("D:/population/countries_2000/population_europe_2000_modified.tif")
    arr_img = tiff_file.ReadAsArray()
    arr_img = arr_img.astype(np.int)
    ravel_arr_img = np.ravel(arr_img)
    ravel_arr_img = ravel_arr_img[ravel_arr_img != -999]
    arr_img = None
    img = None
    
    for i in range(0,nb_iterations+1,1):
        if i <= nb_iterations:
            mat = np.random.choice(ravel_arr_img, (x_size, y_size))
            opti_outputs = Find_opti_bandwidth(input_mat = mat, bw_lower =bw_lower, bw_upper=bw_upper, bw_jump=bw_jump)
            opti_bandwidths.append(opti_outputs[0])
            opti_R_squared.append(opti_outputs[1])
            print("I finish iteration number "+str(i+1))
        else:
            end = time.time()            
            duration = end - start
            print("I made this one in "+str(duration)+" seconds")
    
    return [opti_bandwidths, opti_R_squared]

outputs = random_mat_opti_bandwidths(nb_iterations=4000, x_size = 10, y_size = 10, bw_lower = 1.1, bw_upper = 5.1, bw_jump = 0.1)
list_opti_bandwidths = outputs[0]
list_opti_R_squared = outputs[1]    
print("Average :"+str(mean(list_opti_bandwidths))+" R squared "+str((mean(list_opti_R_squared))))
print("Median :"+str(statistics.median(list_opti_bandwidths))+" R squared "+str(statistics.median(list_opti_R_squared)))
print("Minimum :"+str(min(list_opti_bandwidths))+" R squared "+str(min(list_opti_R_squared)))
print("Maximum :"+str(max(list_opti_bandwidths))+" R squared "+str(max(list_opti_R_squared)))
print("Standard Deviations :"+str(statistics.stdev(list_opti_bandwidths))+" R squared "+str(statistics.stdev(list_opti_R_squared)))
    

"""
mat = np.ones((100,100))
for x in range(0,100,1):
    for y in range(0,100,1):
        mat[x,y] = random.randint(0, 64)

print(Find_opti_bandwidth(input_mat=mat, bw_lower=1.1, bw_upper=2, bw_jump=0.01))
"""

"""
#1. OPEN THE TIFF FILE
tiff_file = gdal.Open("D:/night_light/countries_2000/night_light_europe_2000_modified.tif")

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

final_arr = smooth_matrix(arr_img, 1.7)
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
new_tiff = driver.Create("D:/test/smooth_night_light_bw1_7.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_arr)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file
"""