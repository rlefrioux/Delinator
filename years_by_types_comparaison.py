import sys
import csv
import time
from mpl_toolkits import mplot3d
import pandas as pd
from osgeo import gdal
from csv import reader
import matplotlib.pyplot as plt
import numpy as np
from subprocess import Popen
sys.path.insert(0, "D:/python_script/")
import comparaison
from delineator import delineator



types_list = ["night_light", "built", "population"]
ctr_code = "URY"
ctr_name = "Uruguay"
available_years = {"night_light" : [i for i in range(1992, 2014, 1)], "built" : [1975, 1990, 2000, 2014], "population" : [i for i in range(2000, 2020, 1)]}


for t in types_list:
    for y in available_years[t]:
        input_tiff = "D:/"+t+"/countries_"+str(y)+"/"+t+"_"+ctr_code+"_"+str(y)+".tif"
        for i in range(80, 100 , 1):    
            output_tiff = "D:/test/p"+str(i)+"_"+t+"_"+ctr_code+"_"+str(y)+".tif"
            start = time.time()
            delineator(input_tiff, output_tiff, i)
            end = time.time()
            duration = end-start
            print(duration)


for t in types_list: 
    for i in available_years[t]:
        with open("D:/test/"+ctr_code+"_comparaison_"+t+"_"+str(i)+"_VS_"+str(2000)+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Percentile 1st Map","Type of the 1st Map", "Year 1st Map", "Percentile 2nd Map","Type of the 2nd Map", "Year 2nd Map", "Jaccard Index"])    
            for ii in range(80, 100, 1):
                input_tiff_1 = "D:/test/p"+str(ii)+"_"+t+"_"+ctr_code+"_2000.tif"
                input_tiff_2 = "D:/test/p"+str(ii)+"_"+t+"_"+ctr_code+"_"+str(i)+".tif"
                writer.writerow([str(ii), t, str(i), str(ii), t, str(i), comparaison.jaccard_index(input_tiff_1, input_tiff_2), comparaison.mse(input_tiff_1, input_tiff_2), comparaison.SSIM(input_tiff_1, input_tiff_2)])
          
   
"""
for t in types_list:
    with open("D:/test/"+ctr_code+"_comparaison_"+t+".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Percentile 1st Map","Type of the 1st Map", "Percentile 2nd Map","Type of the 2nd Map", "Jaccard Index"])    
        for i in range(80, 99, 1):
            input_tiff_1 = "D:/test/p"+str(i)+"_"+t+"_"+ctr_code+"_2000.tif"
            input_tiff_2 = "D:/test/p"+str(i+1)+"_"+t+"_"+ctr_code+"_2000.tif"
            writer.writerow([str(i), t, str(i+1), t, jaccard_index(input_tiff_1, input_tiff_2)])


for t in types_list:
    df = pd.read_csv("D:/test/"+ctr_code+"_comparaison_"+t+".csv")
    plt.plot(df["Percentile 1st Map"], 1-df["Jaccard Index"], label=t)

plt.title("Jaccard Index for "+ctr_name, fontweight="bold")
plt.legend(("Night Light", "Built", "Population"))
plt.xlabel("Percentiles", fontsize = "12")
plt.xticks([80, 85, 90, 95, 100])
plt.ylabel("Jaccard Index", fontsize = "12")
plt.savefig("D:/test/"+ctr_code+"_jaccard.png")
plt.show()
plt.close()


for i in range(0, len(types_list), 1):
    for j in range(i+1, len(types_list), 1):
        df = pd.read_csv("D:/test/"+ctr_code+"_comparaison_"+str(types_list[i])+"_VS_"+str(types_list[j])+".csv")
        plt.scatter(df["Percentile 1st Map"], df["Percentile 2nd Map"], s=500, c=df["Jaccard Index"], marker = "s")
        plt.gray()
        plt.colorbar()
        plt.title("Jaccard Index Between "+str(types_list[i])+" and "+str(types_list[j])+" for "+ctr_name, fontweight="bold")
        plt.xlabel("Percentiles in "+str(types_list[i]), fontsize = "12")
        plt.xticks([80, 85, 90, 95, 100])
        plt.ylabel("Percentiles in "+str(types_list[j]), fontsize = "12")
        plt.yticks([80, 85, 90, 95, 100])
        plt.savefig("D:/test/"+ctr_code+"_jaccard_"+str(types_list[i])+"_VS_"+str(types_list[j])+".png")
        plt.close()

"""


