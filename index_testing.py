import math
import numpy as np
from scipy import spatial
from skimage.metrics import structural_similarity as ssim



def jaccard_index(mat_1 , mat_2):
    #Computation of the Jaccard Index
    intersect_mat = mat_1 + mat_2 
    intersect = np.count_nonzero(intersect_mat == 0)
    union = np.count_nonzero(intersect_mat <= 1)
    if union != 0:
        j_index = intersect/union
    else:
        j_index = 0
    return j_index






def windowed_jaccard_index(mat_1, mat_2, bandwidth):
    jaccard_list = []
    global_intersect_mat = mat_1 + mat_2 
    global_union = np.count_nonzero(global_intersect_mat <= 1)

    for x in range(0, mat_1.shape[0], bandwidth):
        for y in range(0, mat_1.shape[1], bandwidth):
            intersect_mat = mat_1[x:x+bandwidth, y:y+bandwidth] + mat_2[x:x+bandwidth, y:y+bandwidth]
            union = np.count_nonzero(intersect_mat <= 1)
            jaccard = jaccard_index(mat_1[x:x+bandwidth, y:y+bandwidth], mat_2[x:x+bandwidth, y:y+bandwidth]) 
            jaccard_list.append(jaccard*(union/global_union))
    
    return sum(jaccard_list)

def SMC(mat_1 , mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n00 = np.count_nonzero(intersect_mat == 0)
   n11 = np.count_nonzero(intersect_mat == 2)
   n01 = np.count_nonzero(intersect_mat == 1)
   if n11+n01 != 0:
       SMC = (n11+n00) / (n11+n01)
   else:
       SMC = 0
   return SMC
    
def kulsinki_index(mat_1 , mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n01 = np.count_nonzero(intersect_mat == 1)
   n11 = np.count_nonzero(intersect_mat == 2)
   n =  np.count_nonzero(intersect_mat != 9)
   if n01+n != 0:
       kulsinki = (n01-n11+n) / (n01+n)
   else:
       kulsinki = 0
   return kulsinki    

def mse(mat_1, mat_2):
    #Computation of the Mean Squared Errors
    err = np.sum((mat_1.astype("float") - mat_2.astype("float")) ** 2)
    err /= float(mat_1.shape[0] * mat_2.shape[1])
    return err    


def rmse(mat_1, mat_2):
    #Computation of the Mean Squared Errors
    err = np.sum((mat_1.astype("float") - mat_2.astype("float")) ** 2)
    err /= float(mat_1.shape[0] * mat_2.shape[1])
    return math.sqrt(err)    

def hamming_distance(mat_1, mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n01 = np.count_nonzero(intersect_mat == 1)
   n = np.count_nonzero(intersect_mat != 9)
   if n != 0:
       hamming = n01 / n
   else:
       hamming = 0
   return hamming    

def dice_distance(mat_1, mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n01 = np.count_nonzero(intersect_mat == 1)
   n11 = np.count_nonzero(intersect_mat == 2)
   if n01 + 2*n11 != 0:
       dice_distance = n01 / n01 + 2*n11
   else:
       dice_distance = 0
   return dice_distance    

def rogerstanimoto_distance(mat_1, mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n01 = np.count_nonzero(intersect_mat == 1)
   n11 = np.count_nonzero(intersect_mat == 2)
   n00 = np.count_nonzero(intersect_mat == 0)
   if n11 + n00 + 2*n01 != 0:
       roger_distance = 2*n01 / n11 + n00 + 2*n01
   else:
       roger_distance = 0
   return roger_distance    

def russellrao_distance(mat_1, mat_2):
   #Computation of the Jaccard Index
   intersect_mat = mat_1 + mat_2 
   n11 = np.count_nonzero(intersect_mat == 2)
   n = np.count_nonzero(intersect_mat != 9)
   if n != 0:
       russelrao_distance = n - n11 / n
   else:
       russelrao_distance = 0
   return russelrao_distance    



original_mat = np.array([[0,0,1,0,0,1],
                [0,0,1,1,1,1],
                [1,1,1,1,0,1],
                [1,1,1,0,0,1],
                [0,1,1,1,0,0],
                [1,1,1,1,0,0]])

mat_A = np.array([[0,0,1,0,0,1],
         [0,0,1,1,1,1],
         [0,0,1,1,0,1],
         [0,0,1,0,0,1],
         [0,1,1,1,0,0],
         [1,1,1,1,0,0]])

mat_B = np.array([[1,1,1,0,0,1],
         [1,1,1,1,1,1],
         [1,1,1,1,0,1],
         [1,1,1,0,0,1],
         [0,1,1,1,0,0],
         [1,1,1,1,0,0]])


print("Jaccard Index when an area is bigger: "+str(round(jaccard_index(original_mat, mat_A),3)))
print("Jaccard Index when an area is missing: "+str(round(jaccard_index(original_mat, mat_B),3)))


print("SCM when an area is bigger: "+str(round(SMC(original_mat, mat_A),3)))
print("SCM when an area is missing: "+str(round(SMC(original_mat, mat_B),3)))

print("Kulsinki Index when an area is bigger: "+str(round(kulsinki_index(original_mat, mat_A),3)))
print("Kulsinki Index when an area is missing: "+str(round(kulsinki_index(original_mat, mat_B),3)))

print("MSE when an area is bigger: "+str(round(mse(original_mat, mat_A),3)))
print("MSE when an area is missing: "+str(round(mse(original_mat, mat_B),3)))

print("RMSE when an area is bigger: "+str(round(rmse(original_mat, mat_A),3)))
print("RMSE when an area is missing: "+str(round(rmse(original_mat, mat_B),3)))


print("Hamming distance when an area is bigger: "+str(round(hamming_distance(original_mat, mat_A),3)))
print("Hamming distance when an area is missing: "+str(round(hamming_distance(original_mat, mat_B),3)))

print("Dice distance when an area is bigger: "+str(round(dice_distance(original_mat, mat_A),3)))
print("Dice distance when an area is missing: "+str(round(dice_distance(original_mat, mat_B),3)))

print("Rogerstanimoto distance when an area is bigger: "+str(round(rogerstanimoto_distance(original_mat, mat_A),3)))
print("Rogerstanimoto distance when an area is missing: "+str(round(rogerstanimoto_distance(original_mat, mat_B),3)))

print("Russellrao distance when an area is bigger: "+str(round(russellrao_distance(original_mat, mat_A),3)))
print("Russellrao distance when an area is missing: "+str(round(russellrao_distance(original_mat, mat_B),3)))



