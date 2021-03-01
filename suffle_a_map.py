import numpy as np
from osgeo import gdal
from osgeo import osr


#open a tiff file

tiff_file = gdal.Open("D:/night_light/countries_2000/night_light_europe_2000_modified.tif")
arr_img = tiff_file.ReadAsArray()

