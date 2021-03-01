import numpy as np
from osgeo import gdal
from osgeo import osr
import scipy
from scipy import stats

#open a tiff file

tiff_file = gdal.Open("D:/sedac_population/countries_2000/sedac_population_europe_2000_modified.tif")

geotransform = tiff_file.GetGeoTransform()
projection = tiff_file.GetProjection()
band = tiff_file.GetRasterBand(1)    
xsize = band.XSize
ysize = band.YSize

#3. LOAD THE TIFF FILE IN AN ARRAY

arr_img = tiff_file.ReadAsArray()
tiff_file = None #close it
band = None #close it

mat_se = np.std(np.select(arr_img>=0, arr_img))
final_arr = scipy.ndimage.filters.gaussian_filter(arr_img, mat_se, order=0, output=None, mode='constant', cval=-999, truncate=4.0)
 
driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/lul.tif" ,xsize,ysize,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(final_arr)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file

