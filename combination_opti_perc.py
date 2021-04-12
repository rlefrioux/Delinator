import numpy as np
from osgeo import gdal


index_list = ["jaccard", ]
types_list = ["night_light", "built", "population"]
opti_perc_list = [95, 95, 96]

#COMBINE OPTIMAL MAPS USING PIXELS THAT ARE URBAN ON ALL MAPS

#Load tiff files and their properties
tiff_file_1 = gdal.Open("D:/test/europe/p93_night_light_europe_2000.tif")
geotransform = tiff_file_1.GetGeoTransform()
projection = tiff_file_1.GetProjection()
band = tiff_file_1.GetRasterBand(1)    
xsize = band.XSize
ysize = band.YSize
arr_img_1 = tiff_file_1.ReadAsArray()
tiff_file_1 = None

tiff_file_2 = gdal.Open("D:/test/europe/p95_built_europe_2000.tif")
arr_img_2 = tiff_file_2.ReadAsArray()
tiff_file_2 = None

tiff_file_3 = gdal.Open("D:/test/europe/p96_population_europe_2000.tif")
arr_img_3 = tiff_file_3.ReadAsArray()
tiff_file_3 = None

#Create a matrix with value 0 when pixels are urban on all maps 
urban_matrice = arr_img_1 + arr_img_2 + arr_img_3
final_map = np.where(urban_matrice==0, 0, 1) 

#Create the tiff file and save it 
driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/Europe/optimal_europe_all_maps.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_map)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file


#COMBINE OPTIMAL MAPS USING PIXELS THAT ARE URBAN ON ALL MAPS

#Load tiff files and their properties
tiff_file_1 = gdal.Open("D:/test/europe/p93_night_light_europe_2000.tif")
geotransform = tiff_file_1.GetGeoTransform()
projection = tiff_file_1.GetProjection()
band = tiff_file_1.GetRasterBand(1)    
xsize = band.XSize
ysize = band.YSize
arr_img_1 = tiff_file_1.ReadAsArray()
tiff_file_1 = None

tiff_file_2 = gdal.Open("D:/test/europe/p95_built_europe_2000.tif")
arr_img_2 = tiff_file_2.ReadAsArray()
tiff_file_2 = None

tiff_file_3 = gdal.Open("D:/test/europe/p96_population_europe_2000.tif")
arr_img_3 = tiff_file_3.ReadAsArray()
tiff_file_3 = None

#Create a matrix with value 0 when pixels are urban on all maps 
urban_matrice = arr_img_1 + arr_img_2 + arr_img_3
final_map = np.where(urban_matrice<=1, 0, 1) 

#Create the tiff file and save it 
driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/Europe/optimal_europe_2_maps.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_map)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file





