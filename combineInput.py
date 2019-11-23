"""
s - 2k
"""
import solver, os
import utils
import random
from student_utils import *

def startGen():
    inputName = "convert.in"
    fileName = "combinedMatrix.in"
    size = 200
    connectivity = 0.5
    
    w = open(fileName,"w+")
    
    input_data1 = utils.read_file("100.in")
    num_of_locations1, num_houses1, list_locations1, list_houses1, starting_car_location1, adjacency_matrix1 = data_parser(input_data1)
    
    input_data2 = utils.read_file("100_double.in")
    num_of_locations2, num_houses2, list_locations2, list_houses2, starting_car_location2, adjacency_matrix2 = data_parser(input_data2)
    
    adj_matrix = []
    for i in range(size):
        adj_matrix.append(['x'] * size)
    for i in range(100):
        for j in range(100):
            adj_matrix[i][j] = adjacency_matrix1[i][j]
    for i in range(100):
        for j in range(100):
            adj_matrix[i+100][j+100] = adjacency_matrix2[i][j]
    
    edgeL = int(np.random.random() * 5)
#    while edgeL == 0:
#        edgeL = int(np.random.random() * 138)
    adj_matrix[50][100] = 5
    adj_matrix[100][50] = 5
            
    for i in range(size):
        for j in range(size):
            if adj_matrix[i][j] == 'x':
                pass
            else:
                adj_matrix[i][j] = int(adj_matrix[i][j])
            adj_matrix[i][j] = str(adj_matrix[i][j])
    for i in range(size):
        w.write(' '.join(adj_matrix[i]) + os.linesep)

if __name__ == '__main__':
    startGen()

