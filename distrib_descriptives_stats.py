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

#OPEN THE TIFF FILE

tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000.tif")

#LOAD THE TIFF FILE IN AN ARRAY

arr_img = tiff_file.ReadAsArray()
arr_img = arr_img.astype(np.int)
tiff_file = None #close it

#ONLY KEEP PIXELs WITH VALUE DIFF FROM -999

arr = np.ravel(arr_img)
arr = np.delete(arr, np.where(arr == -999))

#CREATE DESCRIPTIVES STATS

stats = []

stats.append(round(np.mean(arr),3))
stats.append(round(np.std(arr),3))
stats.append(int(np.sum(arr)))
stats.append(int(np.min(arr)))
stats.append(int(np.quantile(arr, q=0.25)))
stats.append(int(np.quantile(arr, q=0.5)))
stats.append(int(np.quantile(arr, q=0.75)))
stats.append(int(np.quantile(arr, q=0.95)))
stats.append(int(np.quantile(arr, q=0.98)))
stats.append(int(np.quantile(arr, q=0.99)))
stats.append(int(np.max(arr)))

header = ["Avg", "Std", "Sum", "Min", "Q1", "Med", "Q3", "95th perc", "98th perc", "99th perc", "Max"]

df = pd.DataFrame([stats], columns = header)
df.to_latex("D:/figures_latex/des_stats_built_europe_2000.tex", index=False, column_format="|ccccccccccc|")



#DESCRIPTIVE STATS TABLE FOR MULTIPLE MAPS

#OPEN THE TIFF FILE

tiff_file_1 = gdal.Open("D:/slopes/countries/slopes_europe.tif")

tiff_file_2 = gdal.Open("D:/water/countries/water_europe.tif")

tiff_file_3 = gdal.Open("D:/elevation/countries/elevation_europe.tif)

#LOAD THE TIFF FILE IN AN ARRAY

arr_img_1 = tiff_file.ReadAsArray()
arr_img_1 = arr_img.astype(np.int)
tiff_file_1 = None #close it


arr_img_2 = tiff_file.ReadAsArray()
arr_img_2 = arr_img.astype(np.int)
tiff_file_2 = None #close it


arr_img_3 = tiff_file.ReadAsArray()
arr_img_3 = arr_img.astype(np.int)
tiff_file_3 = None #close it

#ONLY KEEP PIXELs WITH VALUE DIFF FROM -999

arr_1 = np.ravel(arr_img_1)
arr_1 = np.delete(arr_1, np.where(arr_1 == -999))

arr_2 = np.ravel(arr_img_2)
arr_2 = np.delete(arr_2, np.where(arr_2 == -999))

arr_3 = np.ravel(arr_img_3)
arr_3 = np.delete(arr_3, np.where(arr_3 == -999))

#CREATE DESCRIPTIVES STATS

stats_1 = []

stats.append(round(np.mean(arr_1),3))
stats.append(round(np.std(arr_1),3))
stats.append(int(np.sum(arr_1)))
stats.append(int(np.min(arr_1)))
stats.append(int(np.quantile(arr_1, q=0.25)))
stats.append(int(np.quantile(arr_1, q=0.5)))
stats.append(int(np.quantile(arr_1, q=0.75)))
stats.append(int(np.quantile(arr_1, q=0.95)))
stats.append(int(np.quantile(arr_1, q=0.98)))
stats.append(int(np.quantile(arr_1, q=0.99)))
stats.append(int(np.max(arr_1)))

stats_2 = []

stats.append(round(np.mean(arr_2),3))
stats.append(round(np.std(arr_2),3))
stats.append(int(np.sum(arr_2)))
stats.append(int(np.min(arr_2)))
stats.append(int(np.quantile(arr_2, q=0.25)))
stats.append(int(np.quantile(arr_2, q=0.5)))
stats.append(int(np.quantile(arr_2, q=0.75)))
stats.append(int(np.quantile(arr_2, q=0.95)))
stats.append(int(np.quantile(arr_2, q=0.98)))
stats.append(int(np.quantile(arr_2, q=0.99)))
stats.append(int(np.max(arr_2)))

stats_3 = []

stats.append(round(np.mean(arr_3),3))
stats.append(round(np.std(arr_3),3))
stats.append(int(np.sum(arr_3)))
stats.append(int(np.min(arr_3)))
stats.append(int(np.quantile(arr_3, q=0.25)))
stats.append(int(np.quantile(arr_3, q=0.5)))
stats.append(int(np.quantile(arr_3, q=0.75)))
stats.append(int(np.quantile(arr_3, q=0.95)))
stats.append(int(np.quantile(arr_3, q=0.98)))
stats.append(int(np.quantile(arr_3, q=0.99)))
stats.append(int(np.max(arr_3)))




header = ["Avg", "Std", "Sum", "Min", "Q1", "Med", "Q3", "95th perc", "98th perc", "99th perc", "Max"]

df = pd.DataFrame([stats], columns = header)
df.to_latex("D:/figures_latex/des_stats_built_europe_2000.tex", index=False, column_format="|ccccccccccc|")




















