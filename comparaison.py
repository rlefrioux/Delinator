import numpy as np
import pandas as pd
from osgeo import gdal
from neupy import algorithms
import skimage.measure
from skimage.metrics import structural_similarity as ssim
from osgeo import osr
    
def jaccard_index(first_tiff , second_tiff):
    #Load tiff files in numpy arrays
    tiff_file_1 = gdal.Open(first_tiff)
    arr_img_1 = tiff_file_1.ReadAsArray()
    tiff_file_1 = None
    tiff_file_2 = gdal.Open(second_tiff)
    arr_img_2 = tiff_file_2.ReadAsArray()
    tiff_file_2 = None
    #Computation of the Jaccard Index
    intersect_mat = arr_img_1 + arr_img_2 
    intersect = np.count_nonzero(intersect_mat == 0)
    union = np.count_nonzero(intersect_mat <= 1)
    j_index = intersect/union
    return j_index
    
def mse(first_tiff, second_tiff):
    #Load tiff files in numpy arrays
    tiff_file_1 = gdal.Open(first_tiff)
    arr_img_1 = tiff_file_1.ReadAsArray()
    tiff_file_1 = None
    tiff_file_2 = gdal.Open(second_tiff)
    arr_img_2 = tiff_file_2.ReadAsArray()
    tiff_file_2 = None
    #Computation of the Mean Squared Errors
    err = np.sum((arr_img_1.astype("float") - arr_img_2.astype("float")) ** 2)
    err /= float(arr_img_1.shape[0] * arr_img_2.shape[1])
    return err    


def SSIM(first_tiff, second_tiff):
    #Load tiff files in numpy arrays
    tiff_file_1 = gdal.Open(first_tiff)
    arr_img_1 = tiff_file_1.ReadAsArray()
    tiff_file_1 = None
    tiff_file_2 = gdal.Open(second_tiff)
    arr_img_2 = tiff_file_2.ReadAsArray()
    tiff_file_2 = None
    #Computation of the SSIM 
    SSIM = ssim(arr_img_1, arr_img_2) 
    return SSIM 




