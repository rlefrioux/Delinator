import csv
import subprocess

continents = ["europe", ]

for y in [2000, 2005, 2010, 2015, 2020]:
    for c in continents:
        command = "gdalwarp -t_srs EPSG:4326 -te_srs EPSG:4326 -tr 0.008333333300000000596 0.008333333300000000596 -of GTiff -overwrite -cutline D:/country_boundaries/"+c+".shp -cl "+c+" -crop_to_cutline -dstnodata -999.0 D:/sedac_population/sedac_population_"+str(y)+".tif D:/sedac_population/countries_"+str(y)+"/sedac_population_"+c+"_"+str(y)+".tif"
        proc = subprocess.Popen(command, shell=True)
        print("J'en ai fini avec "+ str(y) + c)

