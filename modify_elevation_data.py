import numpy as np 
from osgeo import gdal
from osgeo import osr


input_tiff = "D:/elevation/elevation.tif"
output_tiff = "D:/elevation/elevation_modified.tif"

#1. OPEN THE TIFF FILE
tiff_file = gdal.Open(input_tiff)

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


#Operation on the array

min_value = arr_img.min()
arr_img_modified = arr_img - min_value

#save the new array in a tiff file

driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(arr_img_modified)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file