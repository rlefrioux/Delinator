import numpy as np 
from osgeo import gdal
from osgeo import osr


#This function create a binary map where 0 value indicate that the pixel can't be urban
 
def cant_be_urban(input_tiff, output_tiff, threshold):
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
    
 
    perc = np.percentile(np.select(arr_img>=0, arr_img) , 99, interpolation = 'nearest')
    
    final_arr = np.where(arr_img <= threshold, -2, arr_img)
    final_arr = np.where(final_arr > 0, 0, final_arr) 
    final_arr = np.where(final_arr != 0, 1, final_arr)

    
    #save the new array in a tiff file
    
    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file
    

thresholds_dict = {"water" : (0.424/4), "slopes" : 21, "elevation" : 1213+412}
topo_map = ["water", "slopes", "elevation"]

for t in topo_map:
    input_tiff = "D:/"+t+"/countries/"+t+"_europe.tif"
    output_tiff = "D:/"+t+"/countries/binary_"+t+"_europe.tif"
    cant_be_urban(input_tiff, output_tiff, thresholds_dict[t])




def merge_cant_be_urban(tiff_elev_binary, tiff_water_binary, tiff_slopes_binary, output_tiff):
    
    #1. OPEN THE TIFF FILE
    tiff_elev = gdal.Open(tiff_elev_binary)
    tiff_water = gdal.Open(tiff_water_binary)
    tiff_slopes = gdal.Open(tiff_slopes_binary)
    
    #2. GET INFORMATION FROM THE TIFF FILE
    
    geotransform = tiff_elev.GetGeoTransform()
    projection = tiff_elev.GetProjection()
    band = tiff_elev.GetRasterBand(1)    
    xsize = band.XSize
    ysize = band.YSize
    
    #3. LOAD THE TIFF FILE IN AN ARRAY
    
    arr_img_elev = tiff_elev.ReadAsArray()
    arr_img_water = tiff_water.ReadAsArray()
    arr_img_slopes = tiff_slopes.ReadAsArray()
    
    tiff_elev = None #close it
    tiff_water = None #close it
    tiff_slope = None #close it
    
    band = None #close it
    
    #OPERATION ON ARRAYS
    
    arr_img = arr_img_elev + arr_img_water + arr_img_slopes 
    #exclude pixels that can't be urban  from at least one topo characteristics
    final_arr = np.ones(arr_img_water.shape)
    final_arr = np.where(arr_img_elev == -999, -999, final_arr)
    final_arr = np.where(arr_img==3 , 0, 1)
    
    #save the new array in a tiff file
    
    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file

    
tiff_elev_binary = "D:/elevation/countries/binary_elevation_europe.tif"    
tiff_water_binary = "D:/water/countries/binary_water_europe.tif"    
tiff_slopes_binary = "D:/slopes/countries/binary_slopes_europe.tif"    
output_tiff = "D:/none_urban/countries/none_urban_europe.tif"    
    
merge_cant_be_urban(tiff_elev_binary, tiff_water_binary, tiff_slopes_binary, output_tiff)    

def mask_none_urban(none_urban_mask, tiff_to_mask, output_tiff):
     #1. OPEN THE TIFF FILE
    tiff_none_urban = gdal.Open(none_urban_mask)
    tiff_to_modify = gdal.Open(tiff_to_mask)

    #2. GET INFORMATION FROM THE TIFF FILE
    
    geotransform = tiff_none_urban.GetGeoTransform()
    projection = tiff_none_urban.GetProjection()
    band = tiff_none_urban.GetRasterBand(1)    
    xsize = band.XSize
    ysize = band.YSize
    
    #3. LOAD THE TIFF FILE IN AN ARRAY
    
    arr_mask = tiff_none_urban.ReadAsArray()
    arr_img = tiff_to_modify.ReadAsArray()

    
    tiff_none_urban = None #close it
    tiff_to_modify = None #close it

    band = None #close it
    
    #OPERATION ON ARRAYS
    
    #This to reshape the mask in order to fit it with the map
    
    arr_mask = np.delete(arr_mask, 0, axis = 0)
    arr_mask = np.delete(arr_mask, 0, axis = 1)

    #exclude pixels that can't be urban using a mask
    
    final_arr = np.where(arr_mask == 1, 0, arr_img)
    
    #save the new array in a tiff file
    
    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file
    
  
  

none_urban_mask = "D:/none_urban/countries/none_urban_europe.tif"
tiff_to_modify = "D:/population/countries_2019/population_europe_2019.tif"
output_tiff = "D:/population/countries_2019/population_europe_2019_modified.tif"
mask_none_urban(none_urban_mask, tiff_to_modify, output_tiff)




    
