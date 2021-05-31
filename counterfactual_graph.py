from PIL import Image
import numpy as np
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import sys
import seaborn as sns
from zipfile import ZipFile as zf
import copy
import pandas as pd
import time
import json
import concurrent.futures
sys.path.insert(0, "D:/python_script/")
import cluster_maker as cm
import smooth_density as sd


#1. OPEN THE TIFF FILE
tiff_file = gdal.Open("D:/population/countries_2000/population_france_2000.tif")

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


  
with open("D:/test/counterfactuals_outputs/population_counterfactual_dict.json") as f:
    content = f.read()
    value_dict = json.loads(content)
    num_count = 0
    keys = []
    values = []
    for k, v in value_dict.items():
        keys.append(int(k))
        values.append(int(v))

   
values = np.array(values)
values = values.astype(np.ushort)

count_2, bins_count_2 = np.histogram(values, bins=int(np.max(values)))
  
# finding the PDF of the histogram using count values
pdf_2 = count_2 / sum(count_2)
  
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf_2 = np.cumsum(pdf_2)

smooth_mat = sd.smooth_matrix(arr_img, bandwidth=2.3)
ravel_arr_img = np.ravel(smooth_mat)
ravel_arr_img = ravel_arr_img[ravel_arr_img != -999]
ravel_arr_img = np.append(ravel_arr_img, int(np.max(values)))

count_1, bins_count_1 = np.histogram(ravel_arr_img, bins=int(np.max(ravel_arr_img)))
  
# finding the PDF of the histogram using count values
pdf_1 = count_1 / sum(count_1)
  
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf_1 = np.cumsum(pdf_1)
    


plt.plot(bins_count_1[1:], cdf_1, label="CDF", color = "black")
plt.plot(bins_count_2[1:], cdf_2, "--", label="Counterfactual CDF", color = "grey")
plt.legend()
plt.savefig("D:/figures_latex/CDF_population_europe_2019")
plt.close()


"""

smooth_mat = sd.smooth_matrix(arr_img, bandwidth=2.2)

#5.CREATE THE NEW TIFF FILE AND EXPORT IT

driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/figures_latex/smooth_population_map.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(smooth_mat)
new_tiff.FlushCache() #Saves to disk
new_tiff = None #closes the file
 """