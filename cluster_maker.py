import numpy as np

def get_urban_cluster(initial_idx, array):
    to_check = []
    cluster_indexes = set()
    to_check.append(initial_idx)
    
    while len(to_check) > 0:
        idx = to_check.pop()
        cluster_indexes.add(idx)
        x, y = idx
        if x-1>0 and array[x-1,y] == 0 and (x-1,y) not in cluster_indexes:
            to_check.append((x-1,y))
        if y-1>0 and array[x,y-1] == 0 and (x,y-1) not in cluster_indexes:
            to_check.append((x,y-1))
        if x+1<array.shape[0] and array[x+1,y] == 0 and (x+1,y) not in cluster_indexes:
            to_check.append((x+1,y))
        if y+1<array.shape[1] and array[x,y+1] == 0 and (x,y+1) not in cluster_indexes:
            to_check.append((x,y+1))
    
    return cluster_indexes

def get_all_urban_cluster(array):
    classified_idx = set()
    clusters = []
    for x, y in zip(*np.where(array == 0)):
        if (x, y) not in classified_idx:
            cluster = get_urban_cluster((x,y), array)
            for idx in cluster:
                classified_idx.add(idx)
            clusters.append(cluster)
    return clusters

