import numpy as np
from osgeo import gdal
from osgeo import osr

def merge_3_output(tiff_1, tiff_2, tiff_3, output_tiff):
    tiff_1 = gdal.Open(tiff_1)
        
    #2. GET INFORMATION FROM THE TIFF FILE

    geotransform = tiff_1.GetGeoTransform()
    projection = tiff_1.GetProjection()
    band = tiff_1.GetRasterBand(1)    
    xsize = band.XSize
    ysize = band.YSize

    #3. LOAD THE TIFF FILE IN AN ARRAY

    arr_img_1 = tiff_1.ReadAsArray()
    arr_img_1 = arr_img_1.astype(np.int)
    tiff_1 = None #close it
    band = None #close it
    
    #Load the two other tiff files
    
    tiff_2 = gdal.Open(tiff_2)
    arr_img_2 = tiff_2.ReadAsArray()
    arr_img_2 = arr_img_2.astype(np.int)
    tiff_2 = None #close it        
    
    tiff_3 = gdal.Open(tiff_3)
    arr_img_3 = tiff_3.ReadAsArray()
    arr_img_3 = arr_img_3.astype(np.int)
    tiff_3 = None #close it
    
    ########
    
    final_arr = arr_img_1 + arr_img_2 + arr_img_3
    final_arr = np.where(final_arr != 0, 1, final_arr)
    final_arr = np.where(arr_img_1 == -999, -999, final_arr)
    
    ########
    
    driver = gdal.GetDriverByName('GTiff')
    new_tiff = driver.Create(output_tiff ,xsize,ysize,1,gdal.GDT_Int16)
    new_tiff.SetGeoTransform(geotransform)
    new_tiff.SetProjection(projection)
    new_tiff.GetRasterBand(1).WriteArray(final_arr)
    new_tiff.FlushCache() #Saves to disk 
    new_tiff = None #closes the file
    
    
merge_3_output(tiff_1 = "D:/test/population_bw3_p99.tif", tiff_2 = "D:/test/night_light_bw3_p99.tif", tiff_3 = "D:/test/built_bw3_p99.tif", output_tiff="D:/test/bw3_p99_merge.tif") 

   