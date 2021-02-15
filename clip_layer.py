import csv
import subprocess

continents = ["africa", "north_america", "oceania", "south_america", "europe", "asia"]

for y in [1975, 1990, 2000, 2014]:
    for c in continents:
        command = "gdalwarp -t_srs EPSG:4326 -te_srs EPSG:4326 -tr 0.008333333300000000596 0.008333333300000000596 -of GTiff -overwrite -cutline D:/country_boundaries/"+c+".shp -cl "+c+" -crop_to_cutline -dstnodata -999.0 D:/built/GHS_built_"+str(y)+"_allign.tif D:/built/countries_"+str(y)+"/built_"+c+"_"+str(y)+".tif"
        proc = subprocess.Popen(command, shell=True)
        print("J'en ai fini avec "+ str(y) + c)

