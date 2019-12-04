import sys
sys.path.append('..')
sys.path.append('../..')
import random

#This is the implementation of the algorithm from textbook 9.2.2
def kcluster(dijkstra_result, number_of_houses, list_of_houses, k):
    x = random.randrange(0, number_of_houses, 1)
    result = [[]*k]
    centers = [list_of_houses[x]]
    num_centers = 1
    result[num_centers - 1] += [list_of_houses[x]]
    hash = [0] * number_of_houses
    hash[list_of_houses[x]] = 1
    for i in range(2, k + 1):
        max_dis = 0
        next_center = 0
        for j in list_of_houses:
            if hash[j] == 1:
                continue
            min_dis = float('inf')
            for k in centers:
                if dijkstra_result[k][1][0].get[j] < min_dis:
                    min_dis = dijkstra_result[k][1][0].get[j]
            if min_dis > max_dis:
                max_dis = min_dis
                next_center = j
        hash[next_center] = 1
        num_centers += 1
        centers += [next_center]
        result[num_centers - 1] += [next_center]
    for i in list_of_houses:
        if hash[i] == 1:
            continue
        dis = float('inf')
        cluster_to_join = 0
        for j in range(len(centers)):
            if dijkstra_result[centers[j]][1][0].get[i] < dis:
                dis = dijkstra_result[centers[j]][1][0].get[i]
                cluster_to_join = j
        result[cluster_to_join] += [i]
        hash[i] = 1
    return result
