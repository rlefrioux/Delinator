import csv
from osgeo import gdal
from osgeo import osr
import statistics as stat
import sys
import time
import copy
import pandas as pd
import math
import numpy as np
import pickle
sys.path.insert(0, "D:/python_script/")
import cluster_maker as cm

#This function return polar coordinates in matrix coordinates
def world_to_pixel(geo_matrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ul_x= geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    pixel = int((x - ul_x) / x_dist)
    line = -int((ul_y - y) / y_dist)
    return (line, pixel)


def cluster_distributions(output_file, tiff_cluster, tiff_built, tiff_night_light, tiff_population, cities_csv):
    #LOADING OF THE CLUSTERS MAP
    tiff_file = gdal.Open(tiff_cluster)
    arr_img = tiff_file.ReadAsArray()
    arr_img = arr_img.astype(np.int)
    tiff_file = None #close it
    band = None #close it
    
    #DEFINITION OF THE DIFFERENT COORDINATES OF CLUSTERS
    
    arr_img = np.where(arr_img==-1, 0, arr_img)
    arr_img = np.where(arr_img==-999, 1, arr_img)
    clusters_list = cm.get_all_urban_cluster(arr_img)
    
    #LOADING OF THE DIFFERENT OUTPUTS
    tiff_file = gdal.Open(tiff_built)
    arr_built = tiff_file.ReadAsArray()
    arr_built = np.where(arr_built == -999, 0, arr_built)
    
    tiff_file = gdal.Open(tiff_night_light)
    arr_night_light = tiff_file.ReadAsArray()
    arr_night_light = np.where(arr_night_light == -999, 0, arr_night_light)
    
    tiff_file = gdal.Open(tiff_population)
    arr_population = tiff_file.ReadAsArray()
    tiff_file = None
    arr_population = np.where(arr_population == -999, 0, arr_population)
    
    #CREATION OF DISTRIBUTIONS FOR EACH CLUSTERS 
    clusters=[]
    for c in clusters_list:
        if len(c)>1:
            cluster = {}
            cluster["coordinates"] = c
            built_density = []
            night_light_density = []
            population_density = []
            for x,y in c:
                built_density.append(arr_built[x,y])
                night_light_density.append(arr_night_light[x,y])
                population_density.append(arr_population[x,y])
            cluster["built density"] = built_density        
            cluster["night light density"] = night_light_density        
            cluster["population density"] = population_density        
            clusters.append(cluster)
            
    #NAMING OF CLUSTERS
    #Load a geo matrix from a tiff
    
    tiff_file = gdal.Open(tiff_cluster)
    geo_matrix = tiff_file.GetGeoTransform()    

    #open the csv that stores the different cities and their coordinates
    #Notice that the csv should be decreasinly ordered 
    df = pd.read_csv(cities_csv, header=0)
        
    for c in clusters:
        start = time.time()
        for _, row in df.iterrows():
            city_coordinates = set()
            city_coordinates.add(world_to_pixel(geo_matrix, row["long"], row["lat"]))       
            if len(c["coordinates"].intersection(city_coordinates))>0:
                clusters[clusters.index(c)]["name"] = row["com_nom"]
                clusters[clusters.index(c)]["country"] = row["country"]
                print("OK")
                break
        #some clusters do not match with city
        if "name" not in c:
            clusters[clusters.index(c)]["name"] = "NO WHERE"
            clusters[clusters.index(c)]["country"] = "NO WHERE"
            print("NO WHERE")
        end = time.time()
        print(end-start)
    # output_file should have extension .pkl
    with open(output_file, "wb") as f:
        f.write(pickle.dumps(clusters))

    return clusters







    
#Create a list of clusters
output_file = "D:/test/europe_2019/population_2019_clusters_distrib_p99_p99.pkl"
cities_csv = "D:/city_coordinates/europe_city.csv"
tiff_cluster = "D:/test/europe_2019/population_europe_2019_p99_p99.tif"
tiff_built = "D:/built/countries_2000/built_europe_2000.tif"
tiff_night_light = "D:/night_light/countries_2000/night_light_europe_2000.tif"
tiff_population = "D:/population/countries_2000/population_europe_2000.tif"
clusters_built_p98_p98 = cluster_distributions(output_file, tiff_cluster, tiff_built, tiff_night_light, tiff_population, cities_csv)


#CREATE A TABLE
#Create statistics for each clusters on a map

#This is for load an old pickle file
with open("D:/test/europe_2019/population_2019_clusters_distrib_p99_p99.pkl", "rb") as f:
    clusters_built_p98_p98 = pickle.load(f)


clusters_stats = []

for c in clusters_built_p98_p98:
    stats = []
    #Country
    stats.append(c["country"])
    #City name
    stats.append(c["name"])
    #pixels
    stats.append(len(c["coordinates"]))
    #built statistics
    stats.append(round(np.mean(c["built density"]),3)) 
    stats.append(int(np.sum(c["built density"])))
    #night light statistics
    stats.append(round(np.mean(c["night light density"]),3))
    stats.append(int(np.sum(c["night light density"])))
    #population statistics
    stats.append(round(np.mean(c["population density"]),3)) 
    stats.append(int(np.sum(c["population density"])))
    clusters_stats.append(stats)


#store the statistics in a pandas dataframe
#Create a multicolumn header

header = [("","Countries"),("","Names"),("","Sizes")]

list_type = ["Built" , "Night Light", "Population"]
list_stats = ["Avg", "Sum"]

for t in list_type:
    for s in list_stats:
        header.append((t,s))

header = pd.MultiIndex.from_tuples(header)

#create a dataframe with multiple hearder
df = pd.DataFrame(clusters_stats)
#sort by sizes
df = df.sort_values(by=2, ascending=False)

df = pd.DataFrame(df.values.tolist(), columns = header)

#create a latex table with the 2 biggest cities
df.head(20).to_latex("D:/test/europe_2019/stats_population_europe_2019_p99_p99.tex", index=False, multicolumn_format="|c|", column_format="|llc|cc|cc|cc|")







"""
#TO MERGE OVERLAPING CLUSTERS OF TWO DIFFERENT DELINEATION
#create a matrix where values indicate the number of pixel that are overlaping
overlaping_matrix = np.zeros((len(clusters_built_p98_p98),len(clusters_built_p99_p99)))
for i, c in enumerate(clusters_built_p98_p98):
    for j, d in enumerate(clusters_built_p99_p99):
        overlaping_matrix[i,j] = len(c["coordinates"].intersection(d["coordinates"]))


merge_clusters = []     

for i in range(len(clusters_built_p98_p98)):
    cluster = {}
    cluster["larger"] = clusters_built_p98_p98[i]
    cluster["smallers"] = {"coordinates":set(), "built density":[],
                                "night light density":[], "population density":[]}
    for j in range(len(clusters_built_p99_p99)):
        if overlaping_matrix[i,j] > 0:
            cluster["smallers"]["coordinates"] = cluster["smallers"]["coordinates"].union(clusters_built_p99_p99[j]["coordinates"])
            cluster["smallers"]["built density"] += clusters_built_p99_p99[j]["built density"]
            cluster["smallers"]["night light density"] += clusters_built_p99_p99[j]["night light density"]
            cluster["smallers"]["population density"] += clusters_built_p99_p99[j]["population density"]
    merge_clusters.append(cluster)            
"""        
        
        

