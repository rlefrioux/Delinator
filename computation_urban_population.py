import numpy as np
from osgeo import gdal
import sys
import pylatex
from osgeo import osr
sys.path.insert(0, "D:/python_script/")
import cluster_maker as cm


perc = []
urban_population = []
urban_avg_population = []

urban_built = []
urban_avg_built = []

urban_night_light = []
urban_avg_night_light = []

nb_clusters = []
list_nb_urban_pixel = []


#DELINEATIONS STATISTICS

tiff_list = ["population_delineations/population_delineation_p99_p99.tif", 
             "europe_2019/population_europe_2019_p99_p99.tif"]

for f in tiff_list:    
    tiff_file = gdal.Open("D:/test/"+f)
    arr = tiff_file.ReadAsArray()
    arr = arr.astype(np.int)
    urban_arr = np.where(arr==-999, 1, arr)
    urban_arr = np.where(arr == -1, 0 , 1)
    
    #CLUSTERS
    #Number of clusters    
    urban_clusters = cm.get_all_urban_cluster(urban_arr)
    nb_clusters.append(len(urban_clusters))
    
    
    #Number of urban pixels
    
    nb_urban_pixel = np.sum(np.where(urban_arr==0, 1, 0))
    list_nb_urban_pixel.append(nb_urban_pixel)
    
    
    #POPULATION
    
    tiff_file = gdal.Open("D:/population/countries_2000/population_europe_2000.tif")
    arr_pop = tiff_file.ReadAsArray()
    arr_pop = arr_pop.astype(np.int)
    
    
    #computation of the urban population 
    
    urb_pop = np.sum(np.where(urban_arr==0, arr_pop, 0)) 
    urban_population.append(urb_pop)
    
    #computation of the average urban population
    
    masked_array = np.ma.masked_array(arr_pop, mask = urban_arr) 
    avg_urban_pop = masked_array.mean()
    urban_avg_population.append(round(avg_urban_pop, 3))
    

    
    #BUILT
    
    tiff_file = gdal.Open("D:/built/countries_2000/built_europe_2000.tif")
    arr_bui = tiff_file.ReadAsArray()
    arr_bui = arr_bui.astype(np.int)
    
    
    #computation of the urban built
    
    urb_bui = np.sum(np.where(urban_arr==0, arr_bui, 0)) 
    urban_built.append(urb_bui)
    
    
    #computation of the average urban built
    
    masked_array = np.ma.masked_array(arr_bui, mask = urban_arr) 
    avg_urban_bui = masked_array.mean()
    urban_avg_built.append(round(avg_urban_bui, 3))
    
        
    #NIGHT LIGHT
    
    tiff_file = gdal.Open("D:/night_light/countries_2000/night_light_europe_2000.tif")
    arr_NL = tiff_file.ReadAsArray()
    arr_NL = arr_NL.astype(np.int)
    
    
    #computation of the urban night light 
    
    urb_NL = np.sum(np.where(urban_arr==0, arr_NL, 0)) 
    urban_night_light.append(urb_NL)
    
        
    #computation of the average urban night light
    
    masked_array = np.ma.masked_array(arr_NL, mask = urban_arr) 
    avg_urban_NL = masked_array.mean()
    urban_avg_night_light.append(round(avg_urban_NL,3))
    

        
doc = pylatex.Document()
table = pylatex.Tabular("|cc|")
table.add_hline()
table.add_row([pylatex.utils.bold("Population p99 p99 2000"), 
               pylatex.utils.bold("Population p99 p99 2019")])
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Urban Population")])
table.add_hline()
table.add_row(urban_population)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Average Urban Population")])
table.add_hline()
table.add_row(urban_avg_population)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Urban Built")])
table.add_hline()
table.add_row(urban_built)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Average Urban Built")])
table.add_hline()
table.add_row(urban_avg_built)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Urban Night Light")])
table.add_hline()
table.add_row(urban_night_light)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Average Urban Night Light")])
table.add_hline()
table.add_row(urban_avg_night_light)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Number of UAs")])
table.add_hline()
table.add_row(nb_clusters)
table.add_hline()
table.add_row([pylatex.MultiColumn(2, align = "|c|", data="Number of Urban Pixels")])
table.add_hline()
table.add_row(list_nb_urban_pixel)
table.add_hline()
doc.append(table)
doc.generate_tex(filepath="D:/figures_latex/des_stats_years")

