import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
from generateOutput import *
import Google_OR
import input_validator
import output_validator
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """

    """
    Potentially use k-cluster to determine the list_of_homes_to_reach
    """
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
    int_adj_matrix = adj_matrix_to_int(adjacency_matrix)

    list_of_homes_to_reach = list_of_homes.copy()
    home_indices_to_reach = set([0]) # Add Soda to much_reach
    for home in list_of_homes_to_reach:
        home_indices_to_reach.add(list_of_locations.index(home))
    home_indices_to_reach = sorted(list(home_indices_to_reach))
    car_cycle_on_subsetTSP = subsetTSP(home_indices_to_reach, int_adj_matrix)
    # if car_cycle_on_subsetTSP:
    #     print("WOWOWOWOWOW Success!")
    #     print(car_cycle_on_subsetTSP)
    #     result_1, result_2, energy = dropoffLocToOutput(car_cycle_on_subsetTSP, shortest_path_info, list_of_homes, list_of_locations)
    #     return [result_1, result_2]

    minEnergy, min_result_1, min_result_2 = float('inf'), None, None
    for k_cluster in range(10):
        car_cycle = Google_OR.main_func(int_adj_matrix, k_cluster)
        result_1, result_2, cur_energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
        if cur_energy < minEnergy:
            pass

    # result_1, result_2, energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)

    return [result_1, result_2]
    

def subsetTSP(list_of_indices, int_adj_matrix):
    reduced_adj_matrix = []
    for i in list_of_indices:
        curRow = []
        for j in list_of_indices:
            curRow.append(int_adj_matrix[i][j])
        reduced_adj_matrix.append(curRow)
    reduced_car_cycle = Google_OR.main_func(reduced_adj_matrix, 1)
    # print("BEGIN")
    # print(reduced_car_cycle)
    # print(reduced_adj_matrix)
    # print("END")
    return reduced_car_cycle


def adj_matrix_to_int(adj_matrix):
    int_adj_matrix = []
    size = len(adj_matrix)
    for i in range(size):
        curRow = []
        for j in range(size):
            dist = adj_matrix[i][j]
            if dist == 'x':
                curRow.append(100000) """ UGH """
            else:
                curRow.append(int(dist))
        int_adj_matrix.append(curRow)

    return int_adj_matrix

def shortest_paths_and_lengths(all_locs, adj_matrix):
    actual_graph, msg = adjacency_matrix_to_graph(adj_matrix)
    # nx.draw_networkx(actual_graph)
    dijkstra_result = nx.all_pairs_dijkstra(actual_graph)
    return dijkstra_result

def generate_all_cycles(all_locs, adj_matrix, starting_car_location, longest_distance):
    visited = [[0 for _ in range(len(adj_matrix))] for _ in range(len(adj_matrix))]
    cycles = []
    start_vertex = 0
    for i in range(len(all_locs)):
        if starting_car_location == all_locs[i]:
            start_vertex = i
            break

    def dfs(node, path, cur_length):
        nonlocal cycles
        nonlocal longest_distance

        # print(cur_length)

        if cur_length > 14:
            return

        if node == start_vertex:
            cycles += [path]

        for i in range(len(adj_matrix[node])):
            next_dist = adj_matrix[node][i]
            # print(next_dist)
            if next_dist is not 'x' and next_dist > longest_distance:
                continue
            if adj_matrix[node][i] is not 'x' and visited[node][i] < 1:
                visited[node][i] += 1
                dfs(i, path+[i], cur_length + 1)
                visited[node][i] -= 1

    dfs(start_vertex, [start_vertex], 0)
    return cycles



"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            # print(node)
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file, 'SOLVING')

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)
    output_validator.validate_output(input_file, output_file, params=params)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
