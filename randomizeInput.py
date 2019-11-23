"""
s - 2k
"""
import solver, os
import utils
import random
from student_utils import *

def startGen():
    inputName = "convert.in"
    fileName = "100_doggy_done.in"
    size = 100
    
    w = open(fileName,"w+")
    input_data = utils.read_file(inputName)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    loc_dict = {}
    for i in range(size):
        loc_dict[list_locations[i]] = i
    randomList = list(range(size))
    np.random.shuffle(randomList)
    randomDict = {}
    for i in range(size):
        randomDict[randomList[i]] = i
    
    adj_matrix_random = []
    for i in range(size):
        adj_matrix_random.append(['x'] * size)
    for i in range(size):
        for j in range(size):
            adj_matrix_random[randomDict[i]][randomDict[j]] = adjacency_matrix[i][j]
    
    w.write(str(size)+os.linesep)
    w.write(str(size // 2)+os.linesep)
    w.write(list_locations[0])
    for loc in list_locations:
        if loc == list_locations[0]:
            continue
        w.write(" %s" % loc)
    w.write(os.linesep)
    randomizedTAs = []
    for TA in list_houses:
        randomizedTAs.append(list_locations[randomDict[loc_dict[TA]]])
    w.write(randomizedTAs[0])
    for i in range(1, len(randomizedTAs)):
        w.write(" " + randomizedTAs[i])
    w.write(os.linesep)
    w.write(starting_car_location+os.linesep)
    for i in range(size):
        for j in range(size):
            if adj_matrix_random[i][j] == 'x':
                pass
            else:
                adj_matrix_random[i][j] = int(adj_matrix_random[i][j])
            adj_matrix_random[i][j] = str(adj_matrix_random[i][j])
    for i in range(size):
        w.write(' '.join(adj_matrix_random[i]) + os.linesep)

if __name__ == '__main__':
    startGen()

