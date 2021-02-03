from PIL import Image
import numpy as np
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import gdal_merge as gm
import sys

#1. OPEN THE TIFF FILE    

tiff_file = gdal.Open("D:/test/switzerland/out_CHE_popu_2000_99.tif")

#2. GET INFORMATION FROM THE TIFF FILE

geotransform = tiff_file.GetGeoTransform()
projection = tiff_file.GetProjection()
band = tiff_file.GetRasterBand(1)    
w = band.XSize
h = band.YSize

#3. LOAD THE TIFF FILE IN AN ARRAY

arr_img = tiff_file.ReadAsArray()
tiff_file = None #close it
band = None #close it

############################
##4.OPERATION ON THE ARRAY##
############################

def get_neighboors(i, j):
    n = []
    for tmp_i, tmp_j in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= tmp_i < h and 0 <= tmp_j < w:
            n += [(tmp_i, tmp_j)]
    return n

def color_inner_zones(map):
    colored_map = [row.copy() for row in map]
    for i in range(h):
        for j in range(w):
            queue = [(i, j)]
            seen = []
            color_it = True
            while len(queue) > 0:
                tmp_i, tmp_j = queue.pop(0)
                if colored_map[tmp_i][tmp_j] == 0:
                    continue
                if (tmp_i, tmp_j) in seen:
                    continue
                seen += [(tmp_i, tmp_j)]
                n = get_neighboors(tmp_i, tmp_j)
                if len(n) < 4 and colored_map[tmp_i][tmp_j] == 1:
                    color_it = False
                    break
                queue += n
            colored_map[i][j] = int(not color_it)
    return colored_map

new_arr = color_inner_zones(arr_img)
new_arr = np.array(new_arr)


#5.CREATE THE NEW TIFF FILE AND EXPORT IT

driver = gdal.GetDriverByName('GTiff')
new_tiff = driver.Create("D:/test/switzerland/mylene_farmer.tif" , w, h,1,gdal.GDT_Int16)
new_tiff.SetGeoTransform(geotransform)
new_tiff.SetProjection(projection)
new_tiff.GetRasterBand(1).WriteArray(new_arr)
new_tiff.FlushCache() #Saves to disk 
new_tiff = None #closes the file

print("J'ai fini :D")



