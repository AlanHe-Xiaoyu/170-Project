import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import random

from student_utils import *
from generateOutput import *
import Google_OR # Source - Google optimization team https://developers.google.com/optimization/routing/vrp
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
    G, message = adjacency_matrix_to_graph(adjacency_matrix)

    # k_cluster_num_upper_bound = len(list_of_homes) // 20 + 1
    k_cluster_num_upper_bound = 2

    """
    Potentially use k-cluster to determine the list_of_homes_to_reach
    """
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
    int_adj_matrix = adj_matrix_to_int(adjacency_matrix)

    min_result_1, min_result_2, minEnergy = None, None, float('inf')

    """
    Baseline 1 : Drop off all @Soda
    """
    car_cycle = [list_of_locations.index(starting_car_location)]
    simple_result_1, simple_result_2, simple_energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    # print('Baseline 1 done')
    min_result_1, min_result_2, minEnergy = simple_result_1, simple_result_2, simple_energy

    # return [min_result_1, min_result_2]

    """
    Baseline 2 : Mindless TSP (Google OR Tool) <<< Baseline 3 if done
    """
    # simple_TSP_car_cycle = Google_OR.main_func(int_adj_matrix, 1)
    # if simple_TSP_car_cycle and is_valid_walk(G, car_cycle):
    #     print("Simple TSP works")
    #     simple_TSP_result_1, simple_TSP_result_2, simple_TSP_cur_energy = dropoffLocToOutput(simple_TSP_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    #     if simple_TSP_cur_energy < minEnergy:
    #         min_result_1, min_result_2, minEnergy = simple_TSP_result_1, simple_TSP_result_2, simple_TSP_cur_energy

    """
    Baseline 3 : Always Send Home
    """
    final_homes_only_car_cycle = alwaysSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info)
    # Begin generation
    send_home_result_1, send_home_result_2, send_home_energy = dropoffLocToOutput(final_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    if send_home_energy < minEnergy:
        min_result_1, min_result_2, minEnergy = send_home_result_1, send_home_result_2, send_home_energy

    # return [min_result_1, min_result_2]

    """
    Soln 4 : randomize
    """
    times = 100
    selectivity_lst = [0.3, 0.5, 0.7, 0.9]
    for selectivity in selectivity_lst:
        for _ in range(times):
            random_homes_only_car_cycle = randomSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info, selectivity)
            random_send_home_result_1, random_send_home_result_2, random_send_home_energy = dropoffLocToOutput(random_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
            if random_send_home_energy < minEnergy:
                print(selectivity, "Success")
                min_result_1, min_result_2, minEnergy = random_send_home_result_1, random_send_home_result_2, random_send_home_energy

    return [min_result_1, min_result_2]




    """
    Advanced methods
    """
    # for k_cluster in range(2, k_cluster_num_upper_bound): # k = 1 already designed above
    #     print("Current k_cluster param =", k_cluster)

    #     car_cycle = Google_OR.main_func(int_adj_matrix, k_cluster)
    #     if is_valid_walk(G, car_cycle):
    #         print(k_cluster, "works")
    #     # print(car_cycle)
    #         result_1, result_2, cur_energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    #         if cur_energy < minEnergy:
    #             min_result_1, min_result_2, minEnergy = result_1, result_2, cur_energy
    #     else:
    #         break

    # result_1, result_2, energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    # return [min_result_1, min_result_2]
    

def subsetTSP(list_of_indices, int_adj_matrix):
    reduced_adj_matrix = []
    for i in list_of_indices:
        curRow = []
        for j in list_of_indices:
            curRow.append(int_adj_matrix[i][j])
        reduced_adj_matrix.append(curRow)
    reduced_car_cycle = Google_OR.main_func(reduced_adj_matrix, 1)
    return reduced_car_cycle

"""
Solution #3
"""
def alwaysSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info):
    return loc_to_go_TSP(list_of_locations, list_of_homes, starting_car_location, shortest_path_info)

"""
Soln #4
"""
def randomSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info, selectivity):
    random_homes_to_go = []
    for home in list_of_homes:
        if random.random() < selectivity:
            random_homes_to_go.append(home)
    # print(random_homes_to_go)
    return alwaysSendHome(list_of_locations, random_homes_to_go, starting_car_location, shortest_path_info)

"""
Helpers
"""
def loc_to_go_TSP(list_of_locations, places_to_TSP, starting_car_location, shortest_path_info):
    starting_idx = list_of_locations.index(starting_car_location)
    homes_indices = [list_of_locations.index(i) for i in places_to_TSP]
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
    homes_only_TSP_car_cycle = Google_OR.main_func(homes_int_adj_matrix, 1)
    _, final_homes_only_car_cycle = getShortestDistAndPath(shortest_path_info, starting_idx, homes_indices[homes_only_TSP_car_cycle[0]])
    for i in range(1, len(homes_only_TSP_car_cycle) - 1):
        prev_car_idx, cur_car_idx = homes_only_TSP_car_cycle[i - 1], homes_only_TSP_car_cycle[i]
        actual_prev_car, actual_cur_car = homes_indices[prev_car_idx], homes_indices[cur_car_idx]
        _, sp_between = getShortestDistAndPath(shortest_path_info, actual_prev_car, actual_cur_car)
        final_homes_only_car_cycle.extend(sp_between[1:])
    _, ending_path = getShortestDistAndPath(shortest_path_info, homes_indices[homes_only_TSP_car_cycle[-2]], starting_idx)
    final_homes_only_car_cycle.extend(ending_path[1:])
    return final_homes_only_car_cycle

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
    # nx.draw_networkx(actual_graph)
    dijkstra_result = nx.all_pairs_dijkstra(actual_graph)
    # for r in dijkstra_result:
    #     print(r[1])
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
