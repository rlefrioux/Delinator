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
import random
from statistics import mean
import time

def smooth_matrix(input_mat):
    start = time.time()
    arr = np.where(input_mat == -999, 0, input_mat)
    std = np.std(input_mat)
    iq = scipy.stats.iqr(input_mat)
    nb_obs = len(input_mat[0])*len(input_mat)
    opti_sigma = 0.9*min([std, iq])*nb_obs**(-1/5)
    print(opti_sigma)
    #Matrix smoothing    
    final_arr = scipy.ndimage.gaussian_filter(arr, opti_sigma)
    final_arr = np.where(input_mat == -999, -999, final_arr)
    final_arr = np.around(final_arr, 0)
    end = time.time()
    duration = end - start
    print("I smoothed it in "+str(duration)+" seconds")
    return final_arr



