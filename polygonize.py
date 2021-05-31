import csv
import subprocess

command = "gdal_polygonize D:/aaaaa.tif D:/OUTPUT.shp -b 1 -mask D:/aaaaa.tif OUTPUT DN"
proc = subprocess.Popen(command, shell=True)




