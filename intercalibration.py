from PIL import Image
import numpy as np
from osgeo import gdal
from osgeo import osr
import sys
import gdal_merge as gm

#This function is create following the methodology of 
#Wu et al. (2013) 

year = [y for y in range(1992, 2013, 1)]
a = [0.8959, 0.6821, 0.9127, 0.4225, 0.3413, 0.9247, 0.3912, 0.9734, 1.2743, 1.3041, 0.9824, 1.0347, 0.9885, 0.9282, 0.9748, 0.9144, 0.8028, 0.8678, 0.7706, 0.9852, 0.8640, 0.5918, 0.9926, 1.1823, 0.7638, 0.6984, 0.9028, 0.8864, 0.9971, 1.4637, 0.8114]
b = [1.0310, 1.1181, 1.0640, 1.3025, 1.3604, 1.0576, 1.3182, 1.0312, 0.9539, 0.9986, 1.1070, 1.0904, 1.0702, 1.0928, 1.0857, 1.1062, 1.0855, 1.0646, 1.0920, 1.1141, 1.1671, 1.2894, 1.1226, 1.0850, 1.1507, 1.2292, 1.1306, 1.1112, 1.0977, 0.9858, 1.0849]
print(year)

for i in range(0, 31, 1):
    tiff_file = gdal.Open("D:/night_light/night_light_"+str(year[i])+".tif")

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

    arr_img = a[i]*(arr_img + 1)**b[i]
    arr_img = arr_img - 1 


    #5.CREATE THE NEW TIFF FILE AND EXPORT IT

    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create("D:/night_light/calibrated_night_light_"+str(year[i])+".tif" ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(arr_img)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file
    print("J'ai fini "+str(year[i]))
print("J'ai tout fini :D")





