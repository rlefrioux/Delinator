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


index_list = ["jaccard", ]
types_list = ["night_light", "built", "population"]
ctr_code = "africa"
ctr_name = "Africa"
index_dict = {"jaccard" : "Jaccard Index", "MSE" : "Mean Squared Errors", "SSIM" : "Structural Similarity"}


#Create a delineation for different percentile thresholds and data types
for t in types_list:
    input_tiff = "D:/"+t+"/countries_2000/"+t+"_"+ctr_code+"_2000.tif"
    for i in range(89, 98, 1):    
        output_tiff = "D:/test/p"+str(i)+"_"+t+"_"+ctr_code+"_2000.tif"
        start = time.time()
        delineator(input_tiff, output_tiff, i)
        end = time.time()
        duration = end-start
        print("I finish the delineation in "+str(duration)+" for "+ctr_name+" using the "+str(i)+" percentile of the distribution of "+t)
      


#Compare the different types of data 
for i in range(0, len(types_list), 1):
    for j in range(i+1, len(types_list), 1):
        with open("D:/test/"+ctr_code+"_comparaison_"+str(types_list[i])+"_VS_"+str(types_list[j])+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Percentile 1st Map", "Type of the 1st Map", "Percentile 2nd Map", "Type of the 2nd Map", "Jaccard Index"])    
            for ii in range(89, 98, 1):
                for jj in range(89, 98, 1):
                    input_tiff_1 = "D:/test/p"+str(ii)+"_"+str(types_list[i])+"_"+ctr_code+"_2000.tif"
                    input_tiff_2 = "D:/test/p"+str(jj)+"_"+str(types_list[j])+"_"+ctr_code+"_2000.tif"
                    writer.writerow([str(ii), str(types_list[i]), str(jj), str(types_list[j]), comparaison.jaccard_index(input_tiff_1, input_tiff_2)])

"""                 
#Compare the different percentile thresholds   
for ii in index_list:    
    for t in types_list:
        with open("D:/test/"+ctr_code+"_comparaison_"+t+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Percentile 1st Map","Type of the 1st Map", "Percentile 2nd Map","Type of the 2nd Map", "Jaccard Index", "Mean Squared Errors", "Structural Similarity"])    
            for i in range(89, 99, 1):
                input_tiff_1 = "D:/test/p"+str(i)+"_"+t+"_"+ctr_code+"_2000.tif"
                input_tiff_2 = "D:/test/p"+str(i+1)+"_"+t+"_"+ctr_code+"_2000.tif"
                writer.writerow([str(i), t, str(i+1), t, comparaison.jaccard_index(input_tiff_1, input_tiff_2)])
"""

#To create a machin that store the couple of percentiles that max indexes

for k in index_list:
    for ii in range(0, len(types_list), 1):
        for jj in range(ii+1, len(types_list), 1):
            df = pd.read_csv("D:/test/"+ctr_code+"_comparaison_"+types_list[ii]+"_VS_"+types_list[jj]+".csv")
            max_df_1 = pd.DataFrame([], columns=["Percentile 1st Map", "max percentile 2nd map", "max_index"])
            max_df_2 = pd.DataFrame([], columns=["Percentile 1st Map", "max percentile 2nd map", "max_index"])
            if k != "MSE":
                for i in range(89, 98, 1):
                    mask = df["Percentile 1st Map"] == i
                    max_value = df[mask][index_dict[k]].max()
                    idx_max = df[mask][index_dict[k]].idxmax()
                    max_info = {
                        "Percentile 1st Map": i,
                        "max percentile 2nd map": df["Percentile 2nd Map"][idx_max],
                        "max_index": max_value
                        }
                    max_df_1 = max_df_1.append(max_info, ignore_index=True)
                    
                for i in range(89, 98, 1):
                    mask = df["Percentile 2nd Map"] == i
                    max_value = df[mask][index_dict[k]].max()
                    idx_max = df[mask][index_dict[k]].idxmax()
                    max_info = {
                            "Percentile 1st Map": i,
                            "max percentile 2nd map": df["Percentile 1st Map"][idx_max],
                            "max_index": max_value
                        }
                    max_df_2 = max_df_2.append(max_info, ignore_index=True)
            else:
                for i in range(89, 98, 1):
                    mask = df["Percentile 1st Map"] == i
                    max_value = df[mask][index_dict[k]].min()
                    idx_max = df[mask][index_dict[k]].idxmin()
                    max_info = {
                        "Percentile 1st Map": i,
                        "max percentile 2nd map": df["Percentile 2nd Map"][idx_max],
                        "max_index": max_value
                        }
                    max_df_1 = max_df_1.append(max_info, ignore_index=True)
                    
                for i in range(89, 98, 1):
                    mask = df["Percentile 2nd Map"] == i
                    max_value = df[mask][index_dict[k]].min()
                    idx_max = df[mask][index_dict[k]].idxmin()
                    max_info = {
                            "Percentile 1st Map": i,
                            "max percentile 2nd map": df["Percentile 1st Map"][idx_max],
                            "max_index": max_value
                        }
                    max_df_2 = max_df_2.append(max_info, ignore_index=True)
            
            #FIND THE COMBINATION OF PERCENTILE THAT MAX THE SIMILARITY
            
            
            
            
            
            
            #CREATE A GRAPHICS THAT SHOW PAIRS OF PERCENTILE THAT MAXIMIZE 
            plt.plot(max_df_1["Percentile 1st Map"], max_df_1["max percentile 2nd map"])
            plt.plot(max_df_2["max percentile 2nd map"], max_df_2["Percentile 1st Map"])
            plt.title(index_dict[k]+" comparaison between "+types_list[ii]+" and "+types_list[jj]+" for "+ctr_name, fontweight="bold", fontsize=14)
            plt.legend(("Perc. max "+types_list[ii]+" VS "+types_list[jj], "Perc. max "+types_list[jj]+" VS "+types_list[ii] ))
            plt.xticks([i for i in range(89, 98, 1)])
            plt.xlabel("Percentile for "+types_list[ii], fontsize = "12")
            plt.ylabel("Percentile for "+types_list[jj], fontsize = "12")
            plt.yticks([i for i in range(89, 98, 1)])
            plt.savefig("D:/test/"+ctr_code+"_"+k+"_"+types_list[ii]+"_VS_"+types_list[jj]+"_max.png")                
            plt.close()
            
           

"""
#Create a graphic using the different indexes based on the comparaison of the percentile
for i in index_list:
    for t in types_list:
        df = pd.read_csv("D:/test/"+ctr_code+"_comparaison_"+t+".csv")
        plt.plot(df["Percentile 1st Map"], df[index_dict[i]], label=t)
    
    plt.title(index_dict[i] + " for "+ctr_name, fontweight="bold", fontsize=14)
    plt.legend(("Night Light", "Built", "Population"))
    plt.xlabel("Percentiles", fontsize = "12")
    plt.xticks([i for i in range(89, 98, 1)])
    plt.ylabel(index_dict[i], fontsize = "12")
    plt.savefig("D:/test/"+ctr_code+"_"+i+".png")
    plt.show()
    plt.close()
"""



#Create a graphic using the different indexes based on the comparaison of the type of data
for ii in index_list:
    for i in range(0, len(types_list), 1):
        for j in range(i+1, len(types_list), 1):
            df = pd.read_csv("D:/test/"+ctr_code+"_comparaison_"+str(types_list[i])+"_VS_"+str(types_list[j])+".csv")
            plt.scatter(df["Percentile 1st Map"], df["Percentile 2nd Map"], s=2000, c=df[index_dict[ii]], marker = "s")
            plt.gray()
            plt.colorbar()
            plt.title(index_dict[ii] +" Between "+str(types_list[i])+" and "+str(types_list[j])+" for "+ctr_name, fontweight="bold", fontsize=10)
            plt.xlabel("Percentiles in "+str(types_list[i]), fontsize = "12")
            plt.xticks([i for i in range(89, 98, 1)])
            plt.ylabel("Percentiles in "+str(types_list[j]), fontsize = "12")
            plt.yticks([i for i in range(89, 98, 1)])
            plt.savefig("D:/test/"+ctr_code+"_"+ii+"_"+str(types_list[i])+"_VS_"+str(types_list[j])+".png")
            plt.close()   



