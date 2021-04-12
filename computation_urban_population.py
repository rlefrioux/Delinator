import numpy as np
from osgeo import gdal
from osgeo import osr

tiff_file = gdal.Open("D:/population/countries_2000/population_europe_2000.tif")
geotransform = tiff_file.GetGeoTransform()
projection = tiff_file.GetProjection()
band = tiff_file.GetRasterBand(1)    
xsize = band.XSize
ysize = band.YSize

arr_img = tiff_file.ReadAsArray()
arr_img = arr_img.astype(np.int)
tiff_file = None #close it
band = None #close it

####
list_ = ["built", "population", "night_light"]

for x in list_:    
    for n in [95, 96, 97, 98, 99]:
  
        tiff_file = gdal.Open("D:/test/"+x+"_delineation_p"+str(n)+".tif")
        mask_arr = tiff_file.ReadAsArray()
        mask_arr = mask_arr.astype(np.int)
        tiff_file = None #close it
        
        final_arr = np.where(mask_arr==1, -999, arr_img)
        
        #####
        driver = gdal.GetDriverByName('GTiff')
        new_tiff = driver.Create("D:/test/"+x+"_population_p"+str(n)+".tif" ,xsize,ysize,1,gdal.GDT_Int16)
        new_tiff.SetGeoTransform(geotransform)
        new_tiff.SetProjection(projection)
        new_tiff.GetRasterBand(1).WriteArray(final_arr)
        new_tiff.FlushCache() #Saves to disk 
        new_tiff = None #closes the file


list_ = ["built", "population", "night_light"]
urban_population = []
all_population = []
urban_share = []


for x in list_: 
    for n in [95, 96, 97, 98, 99]:
        tiff_file = gdal.Open("D:/test/"+x+"_population_p"+str(n)+".tif")
        arr_img = tiff_file.ReadAsArray()
        arr_img = mask_arr.astype(np.int)
        arr_img = np.where(arr_img==-999, 0, arr_img)
        urban_pop = np.sum(arr_img)
        urban_population.append(urban_pop)
        tiff_file = gdal.Open("D:/population/countries_2000/population_europe_2000.tif")
        arr = tiff_file.ReadAsArray()
        arr = mask_arr.astype(np.int)
        arr = np.where(arr==-999, 0, arr)
        all_pop = np.sum(arr)
        all_population.append(all_pop)
        urban_share.append(urban_pop/all_pop)
        
print(urban_population)
print(all_population)
print(urban_share)    

    
    
    
    
    
    
