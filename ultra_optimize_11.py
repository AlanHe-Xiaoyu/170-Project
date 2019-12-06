import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import random
import itertools
random.seed(10)

from KCluster import *
from student_utils import *
from generateOutput import *
import Google_OR # Source - Google optimization team https://developers.google.com/optimization/routing/vrp
import input_validator
import output_validator

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    # return [[0, 3, 63, 12, 92, 53, 29, 95, 29, 53, 96, 86, 63, 22, 43, 26, 67, 90, 45, 66, 45, 90, 67, 26, 43, 22, 64, 8, 31, 41, 31, 8, 64, 0], {63: [57, 30, 23, 61], 22: [21], 0: [79, 18], 3: [72, 40, 44, 39, 89], 67: [33, 71, 67], 43: [19, 43], 45: [45, 49, 73, 20, 32, 48, 81, 93], 90: [90], 26: [26], 66: [66, 36, 97], 8: [17, 8, 83, 91, 68], 31: [31], 41: [41, 38], 12: [12], 92: [92], 53: [53, 55, 13], 96: [96, 99], 86: [86, 10], 29: [29], 95: [28, 95]}]
    
    G, message = adjacency_matrix_to_graph(adjacency_matrix)
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))

    min_a, min_b, min_energy = None, None, float('inf')
    all_ns = list(range(len(list_of_locations)))
    
    pick_front = True
    while len(all_ns) > 0:

        if pick_front:
            n = all_ns.pop(0)
        else:
            n = all_ns.pop()
        pick_front = not pick_front

        print()
        print(n)
        print()
        for subset_homes in list(itertools.combinations(list_of_locations, n)):
            subset_cycle = loc_to_go_TSP(list_of_locations, subset_homes, starting_car_location, shortest_path_info)
            a, b, energy = dropoffLocToOutput(subset_cycle, shortest_path_info, list_of_homes, list_of_locations)
            if energy < min_energy:
                print([a, b])
                min_a, min_b, min_energy = a, b, energy

    return [min_a, min_b]


"""
Helpers
"""
# Better alg now!!!
def loc_to_go_with_indices(list_of_locations, indices_to_TSP, starting_car_location, shortest_path_info):
    starting_idx = list_of_locations.index(starting_car_location)
    homes_indices = [starting_idx] + indices_to_TSP
    num_homes = len(homes_indices)
    homes_int_adj_matrix = []
    for _ in range(num_homes):
        homes_int_adj_matrix.append([None] * num_homes)
    for i in range(num_homes):
        home = homes_indices[i]
        homes_int_adj_matrix[i][i] = 0
        for j in range(i + 1, num_homes):
            dist_ij, _ = getShortestDistAndPath(shortest_path_info, i, j)
            homes_int_adj_matrix[i][j] = homes_int_adj_matrix[j][i] = dist_ij
    raw_TSP_cycle = Google_OR.main_func(homes_int_adj_matrix, 1)
    start_in_TSP_idx = raw_TSP_cycle.index(0) # corresponds to starting_idx in homes_indices
    actual_TSP_cycle = raw_TSP_cycle[start_in_TSP_idx :] + raw_TSP_cycle[1 : start_in_TSP_idx]
    # actual_TSP_cycle should be a cycle start/end in 0, in homes_indices
    translate_to_loc_idx = [homes_indices[i] for i in actual_TSP_cycle] # in list_of_locations, start/end in starting_idx

    first, second = translate_to_loc_idx[0], translate_to_loc_idx[1]
    _, final_homes_only_car_cycle = getShortestDistAndPath(shortest_path_info, first, second)
    for i in range(2, len(translate_to_loc_idx)):
        prev_loc_idx, cur_loc_idx = translate_to_loc_idx[i-1], translate_to_loc_idx[i]
        _, sp_between = getShortestDistAndPath(shortest_path_info, prev_loc_idx, cur_loc_idx)
        final_homes_only_car_cycle.extend(sp_between[1 :])
    return final_homes_only_car_cycle
    
def loc_to_go_TSP(list_of_locations, places_to_TSP, starting_car_location, shortest_path_info):
    homes_indices = [list_of_locations.index(i) for i in places_to_TSP]
    return loc_to_go_with_indices(list_of_locations, homes_indices, starting_car_location, shortest_path_info)


def getShortestDistAndPath(dijkstra_info, i, j):
    pair_info = dijkstra_info[i][1]
    dist, path = pair_info[0][j], pair_info[1][j]
    return [dist, path[:]]

def adj_matrix_to_int(adj_matrix):
    int_adj_matrix = []
    size = len(adj_matrix)
    for i in range(size):
        curRow = []
        for j in range(size):
            dist = adj_matrix[i][j]
            if dist == 'x':
                curRow.append(10000000000000) # UGHH
            else:
                curRow.append(int(dist))
        int_adj_matrix.append(curRow)

    return int_adj_matrix

def shortest_paths_and_lengths(all_locs, adj_matrix):
    actual_graph, msg = adjacency_matrix_to_graph(adj_matrix)
    dijkstra_result = nx.all_pairs_dijkstra(actual_graph)
    return dijkstra_result

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
#        solve_all(input_directory, output_directory, params=args.params)
        try:
            solve_all(input_directory, output_directory, params=args.params)
        except:
            print("Error")
            os.system("python3 ./outputs/removeProcessed.py")
            os.system("python3 ./solver.py --all inputs outputs")
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
