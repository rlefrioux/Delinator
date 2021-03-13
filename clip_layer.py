import csv
import subprocess

continents = ["SWZ", ]

for y in [2000,]:
    for c in continents:
        command = "gdalwarp -t_srs EPSG:4326 -te_srs EPSG:4326 -tr 0.008333333300000000596 0.008333333300000000596 -of GTiff -overwrite -cutline D:/country_boundaries/gadm36_"+c+"_0.shp -cl "+c+" -crop_to_cutline -dstnodata -999.0 D:/built/built_europe_"+str(y)+"_modified.tif D:/built/countries_"+str(y)+"/built_"+c+"_"+str(y)+".tif"
        proc = subprocess.Popen(command, shell=True)
        print("J'en ai fini avec "+ str(y) + c)

