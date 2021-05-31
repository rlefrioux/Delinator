import csv
import subprocess

type_list = ["night_light", "built", "population"]

years = {"night_light" : [i for i in range(1993, 2014)],
        "built" : [2000, 2015],
        "population" : [i for i in range(2000, 2020)]
        }

continents = ["asia", "north_america", "south_america", "europe", "oceania"]

for t in type_list:
    for y in years[t]:
        for c in continents:
            command = "gdalwarp -s_srs EPSG:4326 -t_srs EPSG:4326 -of GTiff -cutline D:/country_boundaries/"+c+".shp -cl "+c+" -crop_to_cutline -dstnodata -999.0 D:/"+t+"/"+t+"_"+str(y)+".tif D:/inputs/"+t+"/"+str(y)+"/"+t+"_"+str(y)+"_"+c+".tif"
            proc = subprocess.Popen(command, shell=True)
            proc.wait()

