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
        mat_size = int(bandwidth)*2 + 1
        mat_weight = np.zeros((mat_size, mat_size))
        x_center = int(mat_size/2)
        y_center = int(mat_size/2)
        for x in range(0, mat_size, 1):
            for y in range(0, mat_size, 1):
                if euclidean_dist(x_center, y_center, x, y)<=bandwidth:
                    mat_weight[x,y] = (1-(euclidean_dist(x_center, y_center, x, y)/bandwidth)**2)**2
    mat_weight[x_center, y_center] = 0
    return mat_weight



#Notice that the bandwidth should be an odd integer
def smooth_matrix(input_mat, bandwidth=None, kernel_matrix=None):
    if bandwidth is None and bisquare_kernel_matrix is None:
        raise Exception("You must provide either bandwidth or bisquare_kernel_matrix")

    arr = np.where(input_mat == -999, 0, input_mat)
    #Matrix smoothing
    if kernel_matrix is None:
        mat_weight = bisquare_kernel_matrix(bandwidth)
    else:
        mat_weight = kernel_matrix

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

def pseudo_R_squared(input_mat, kernel_matrix, x_excluded, y_excluded):
    excluded_mat = np.copy(input_mat)
    excluded_mat[x_excluded, y_excluded] = 0
    excluded_smooth_mat = smooth_matrix(input_mat=excluded_mat, kernel_matrix=kernel_matrix)
    corr = correlation_coefficient(mat_1=excluded_smooth_mat, mat_2=input_mat)
    pseudo_R_squared = corr**2
    return pseudo_R_squared



def avg_R_squared(input_mat, kernel_matrix, x_size, y_size):
    R_squared_list = np.empty((0))
    weight_list = np.empty((0))
    for x in range(0, x_size, 1):
        for y in range(0, y_size, 1):
            if input_mat[x,y] != 0:
                R_squared_list = np.append(R_squared_list, pseudo_R_squared(input_mat=input_mat, kernel_matrix=kernel_matrix, x_excluded=x, y_excluded=y))
                weight_list = np.append(weight_list, input_mat[x,y])
            else:
                R_squared_list = np.append(R_squared_list, 1)
                weight_list = np.append(weight_list, input_mat[x,y])
    weight_sum = weight_list.sum()
    weight_list = weight_list / weight_sum
    avg_R_squared = np.average(R_squared_list, weights=weight_list)
    return avg_R_squared


def Find_opti_bandwidth(input_mat, bw_lower, bw_upper, bw_jump):
    x_size = len(input_mat)
    y_size = len(input_mat[0])
    bandwidth = []
    R_squared_list = np.empty((0))
    for bw in np.arange(bw_lower, bw_upper, bw_jump):
        kernel_matrix = bisquare_kernel_matrix(bw)
        R_squared_list = np.append(R_squared_list, avg_R_squared(input_mat=input_mat, kernel_matrix=kernel_matrix, x_size=x_size, y_size=y_size))
        bandwidth.append(bw)
    max_index = R_squared_list.argmax()
    max_R_squared = R_squared_list[max_index]
    opti_bw = bandwidth[max_index]
    return [opti_bw, max_R_squared]



def random_mat_opti_bandwidths(nb_iterations, x_size, y_size, bw_lower, bw_upper, bw_jump):
    opti_bandwidths = []
    opti_R_squared = []
    mediane_bw = []
    mediane_R2 = []
    mean_bw = []
    mean_R2 = []
    total_duration = 0
    iteration = 0
    start = time.time()
    tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000_modified.tif")
    arr_img = tiff_file.ReadAsArray()
    arr_img = arr_img.astype(np.int)
    ravel_arr_img = np.ravel(arr_img)
    ravel_arr_img = ravel_arr_img[ravel_arr_img != -999]
    arr_img = None
    img = None
    for i in range(1,nb_iterations+1,1): # [GLF] Fix iteration number
        if i % 10 == 0:
            print(f"Iteration {i} / {nb_iterations}")
        mat = np.random.choice(ravel_arr_img, (x_size, y_size))
        opti_outputs = Find_opti_bandwidth(input_mat = mat, bw_lower =bw_lower, bw_upper=bw_upper, bw_jump=bw_jump)
        opti_bandwidths.append(opti_outputs[0])
        opti_R_squared.append(opti_outputs[1])
        mediane_bw.append(statistics.median(opti_bandwidths))
        mediane_R2.append(statistics.median(opti_R_squared))
        mean_bw.append(mean(opti_bandwidths))
        mean_R2.append(mean(opti_R_squared))
    # [GLF] Fix last iteration action
    end = time.time()
    duration = end - start
    total_duration += duration
    print("I finish the whole process in "+str(duration))
    print("Which make an average iterations time of "+str(duration/nb_iterations))
    return [opti_bandwidths, opti_R_squared, mediane_bw, mediane_R2, mean_bw, mean_R2]



def main():
    opti_bandwidths, opti_R_squared, mediane_bw, mediane_R2, mean_bw, mean_R2 = random_mat_opti_bandwidths(nb_iterations=10000, x_size = 10, y_size = 10, bw_lower = 1.1, bw_upper = 5.1, bw_jump = 0.1)
    plt.plot(mediane_bw)
    plt.savefig("D:/test/mediane_bw_built")
    plt.close()
    plt.plot(mediane_R2)
    plt.savefig("D:/test/mediane_R2_built")
    plt.close()
    plt.plot(mean_bw)
    plt.savefig("D:/test/mean_bw_built")
    plt.close()
    plt.plot(mean_R2)
    plt.savefig("D:/test/mean_R2_built")
    plt.close()

if __name__ == "__main__":
    main()
    
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
