import csv
import subprocess

continents = ["africa"]

for y in range(2000, 2020, 1):
    for c in continents:
        command = "gdalwarp -t_srs EPSG:4326 -te_srs EPSG:4326 -tr 0.008333333300000000596 0.008333333300000000596 -of GTiff -overwrite -cutline D:/country_boundaries/"+c+".shp -cl "+c+" -crop_to_cutline -dstnodata -999.0 /vsizip/D:/population/population.zip/population/population_"+str(y)+".tif D:/population/countries_"+str(y)+"/population_"+c+"_"+str(y)+".tif"
        proc = subprocess.Popen(command, shell=True)
        print("J'en ai fini avec "+ str(y) + c)

