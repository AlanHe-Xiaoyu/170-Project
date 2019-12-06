import sys
sys.path.append('..')
sys.path.append('../..')
import random
from solver import *

#This is the implementation of the algorithm from textbook 9.2.2
def kcluster(dijkstra_result, number_of_houses, list_of_houses, k):
    x = random.randrange(0, number_of_houses, 1)
    result = []
    for i in range(k):
        result.append([])
    centers = [list_of_houses[x]]
    num_centers = 1
    result[num_centers - 1] += [list_of_houses[x]]
    hash = [0] * (max(list_of_houses)+1)
    hash[list_of_houses[x]] = 1
    for i in range(2, k + 1):
        max_dis = 0
        next_center = 0
        for j in list_of_houses:
            if hash[j] == 1:
                continue
            min_dis = float('inf')
            for k in centers:
                if dijkstra_result[k][1][0][j] < min_dis:
                    min_dis = dijkstra_result[k][1][0][j]
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
            if dijkstra_result[centers[j]][1][0][i] < dis:
                dis = dijkstra_result[centers[j]][1][0][i]
                cluster_to_join = j
        result[cluster_to_join] += [i]
        hash[i] = 1
    return result, centers


def goodpoints(list_of_houses, dijkstra_result):
    num_locs = len(dijkstra_result)
    hash = [0] * num_locs
    for i1 in range(len(list_of_houses)):
        for j1 in range(i1+1, len(list_of_houses)):
            i = list_of_houses[i1]
            j = list_of_houses[j1]
            if i != j:
                a, path = getShortestDistAndPath(dijkstra_result, i, j)
                for z in range(1, len(path) - 1):
                    v = path[z]
                    hash[v] += 1
    result = []
    for i in range(len(hash)):
        if hash[i] > len(list_of_houses) / 10:
            result += [i]
    return result
