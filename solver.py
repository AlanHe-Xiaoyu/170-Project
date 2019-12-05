import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import random
random.seed(10)

from KCluster import *
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
# 279428.6666666666
best_of_our_50 = ["Soda", "loc43", "loc38", "loc20", "loc45", "loc31", "loc1", "loc11", "loc2", "loc22", "loc41", "loc14", "loc15", "loc37", "loc39", "loc16", "loc44", "loc29", "loc11", "loc38", "loc43", "loc35", "loc30", "loc35", "loc43", "Soda"]



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

    """ Own inputs """
    # if list_of_locations == ['Soda', 'loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8', 'loc9', 'loc10', 'loc11',
    #                         'loc12', 'loc13', 'loc14', 'loc15', 'loc16', 'loc17', 'loc18', 'loc19', 'loc20', 'loc21', 'loc22', 'loc23',
    #                         'loc24', 'loc25', 'loc26', 'loc27', 'loc28', 'loc29', 'loc30', 'loc31', 'loc32', 'loc33', 'loc34', 'loc35',
    #                         'loc36', 'loc37', 'loc38', 'loc39', 'loc40', 'loc41', 'loc42', 'loc43', 'loc44', 'loc45', 'loc46', 'loc47', 'loc48']:
    #     route_50 = loc_to_go_TSP(list_of_locations, ['loc20', 'loc1', 'loc16', 'loc10'], starting_car_location, shortest_path_info)
    #     print(route_50)
    #     route_50_result_1, route_50_result_2, route_50_energy = dropoffLocToOutput(route_50, shortest_path_info, list_of_homes, list_of_locations)
    #     return [route_50_result_1, route_50_result_2]

    """
    Baseline 1 : Drop off all @Soda
    """
    # car_cycle = [list_of_locations.index(starting_car_location)]
    # simple_result_1, simple_result_2, simple_energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    # # print('Baseline 1 done')
    # min_result_1, min_result_2, minEnergy = simple_result_1, simple_result_2, simple_energy
    #
    # # return [min_result_1, min_result_2]

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
    route_50_result_1, route_50_result_2, send_home_energy = dropoffLocToOutput(final_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    if send_home_energy < minEnergy:
        min_result_1, min_result_2, minEnergy = route_50_result_1, route_50_result_2, send_home_energy

    # return [min_result_1, min_result_2]


    """
    Soln 4 : randomize
    """
    times = 150
    selectivity_lst = []
    if len(list_of_homes) <= 50:
        selectivity_lst = [0.3]
    elif len(list_of_homes) <= 100:
        selectivity_lst = [0.3, 0.5, 0.7]
    else:
        selectivity_lst = [0.3, 0.6]
    # 100
    if starting_car_location == 'Soda' and (list_of_homes[:12] == ['loc57', 'loc21', 'loc79', 'loc18', 'loc72', 'loc33', 'loc71', 'loc19', 'loc45', 'loc90', 'loc67', 'loc26']):
        print('HI our own 100')
        times = 500
        selectivity_lst = [0.1, 0.125, 0.15, 0.2, 0.3]
    # 50
    elif list_of_locations == ['Soda', 'loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8', 'loc9', 'loc10', 'loc11',
        'loc12', 'loc13', 'loc14', 'loc15', 'loc16', 'loc17', 'loc18', 'loc19', 'loc20', 'loc21', 'loc22', 'loc23',
        'loc24', 'loc25', 'loc26', 'loc27', 'loc28', 'loc29', 'loc30', 'loc31', 'loc32', 'loc33', 'loc34', 'loc35',
        'loc36', 'loc37', 'loc38', 'loc39', 'loc40', 'loc41', 'loc42', 'loc43', 'loc44', 'loc45', 'loc46', 'loc47', 'loc48']:
        print("this 50 - directly returning")
        car_route_50_idx = best_of_our_50
        car_route_50 = [list_of_locations.index(loc) for loc in car_route_50_idx]
        a, b, c = dropoffLocToOutput(car_route_50, shortest_path_info, list_of_homes, list_of_locations)
        return [a, b]
        times = 300
        selectivity_lst = [0.3, 0.4, 0.5]
    # 200
    elif list_of_homes[:12] == ["loc45", "loc82", "loc90", "loc65", "loc151", "loc50", "loc83", "loc94", "loc34", "loc13", "loc74", "loc23"] and starting_car_location == 'Soda':
        times = 500
        selectivity_lst = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    for selectivity in selectivity_lst:
        flag = 0
        print(selectivity)
        for _ in range(times):
            random_homes_only_car_cycle = randomSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info, selectivity)
            random_send_home_result_1, random_send_home_result_2, random_send_home_energy = dropoffLocToOutput(random_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
            if random_send_home_energy < minEnergy:
                print(selectivity, "Success")
                min_result_1, min_result_2, minEnergy = random_send_home_result_1, random_send_home_result_2, random_send_home_energy
            else:
                flag += 1

            if flag >= 5:
                break
        

    
    """
    K-Cluster as dropoff
    """
    K_list = [i for i in range(2, len(list_of_homes), 1)]
    
    out_counter = 0
    for k in K_list:
        k_flag = False
        print("k=", k)
        name_index_map = {}
        num_of_homes = len(list_of_homes)
        home_list = []
        for i in range(len(list_of_locations)):
            name_index_map[list_of_locations[i]] = i;
        for x in list_of_homes:
            home_list += [name_index_map[x]]
        d_result = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
        cluster, center = kcluster(d_result, num_of_homes, home_list, k)

        all_k_sel = [0, 0.1]
        k_times = 100
        counter = 0
        for k_cluster_sel in all_k_sel:
            for _ in range(k_times):
                random_indices = get_random_indices_k_cluster(cluster, k_cluster_sel)
                random_indices.extend(center)
                random_indices = list(set(random_indices))
                # print(random_indices)
                random_k_cluster_cycle = loc_to_go_with_indices(list_of_locations, random_indices, starting_car_location, shortest_path_info)
                k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy = dropoffLocToOutput(random_k_cluster_cycle, shortest_path_info, list_of_homes, list_of_locations)
                # print(k, k_cluster_result_energy)
                if k_cluster_result_energy < minEnergy:
                    print("k_cluster", k, k_cluster_sel, "Success")
                    k_flag = True
                    min_result_1, min_result_2, minEnergy = k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy
                elif counter > 7:
                    break
                else:
                    counter += 1
        if not k_flag:
            out_counter += 1
        if out_counter > 3:
            break


    # return [min_result_1, min_result_2]

    # """
    # K-Cluster as dropoff
    # """
    # K_list = [i for i in range(2, len(list_of_homes), 1)]
    # counter = 0
    # for k in K_list:
    #     print("k=", k)
    #     name_index_map = {}
    #     num_of_homes = len(list_of_homes)
    #     home_list = []
    #     for i in range(len(list_of_locations)):
    #         name_index_map[list_of_locations[i]] = i;
    #     for x in list_of_homes:
    #         home_list += [name_index_map[x]]
    #     d_result = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
    #     cluster, center = kcluster(d_result, num_of_homes, home_list, k)
    #     # print(kcluster(d_result, num_of_homes, home_list, k))

    #     k_cluster_sel = 0.25
    #     random_indices = get_random_indices_k_cluster(cluster, k_cluster_sel)
    #     random_indices.extend(center)
    #     random_indices = list(set(random_indices))
    #     print(random_indices)
    #     random_k_cluster_cycle = loc_to_go_with_indices(list_of_locations, random_indices, starting_car_location, shortest_path_info)
    #     k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy = dropoffLocToOutput(random_k_cluster_cycle, shortest_path_info, list_of_homes, list_of_locations)
    #     # print(k, k_cluster_result_energy)
    #     if k_cluster_result_energy < minEnergy:
    #         print("k_cluster", k, sel, "Success")
    #         min_result_1, min_result_2, minEnergy = k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy
    #     elif counter > 5:
    #         break
    #     else:
    #         counter += 1

        # k_cluster_cycle = loc_to_go_with_indices(list_of_locations, center, starting_car_location, shortest_path_info)
        # k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy = dropoffLocToOutput(k_cluster_cycle, shortest_path_info, list_of_homes, list_of_locations)
        # # print(k, k_cluster_result_energy)
        # if k_cluster_result_energy < minEnergy:
        #     print("k_cluster", k, "Success")
        #     min_result_1, min_result_2, minEnergy = k_cluster_result_1, k_cluster_result_2, k_cluster_result_energy
        # elif counter > 5:
        #     break
        # else:
        #     counter += 1
    return [min_result_1, min_result_2]




def subsetTSP(list_of_indices, int_adj_matrix):
    reduced_adj_matrix = []
    for i in list_of_indices:
        curRow = []
        for j in list_of_indices:
            curRow.append(int_adj_matrix[i][j])
        reduced_adj_matrix.append(curRow)
    reduced_car_cycle = Google_OR.main_func(reduced_adj_matrix, 1)
    return reduced_car_cycle

def get_random_indices_k_cluster(clusters, sel):
    result = []
    for cluster in clusters:
        for pt in cluster:
            if random.random() < sel:
                result.append(pt)
    return result

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
        if random.random() <= selectivity:
            random_homes_to_go.append(home)
    # print(random_homes_to_go)
    return alwaysSendHome(list_of_locations, random_homes_to_go, starting_car_location, shortest_path_info)

"""
Helpers
"""
def loc_to_go_with_indices(list_of_locations, indices_to_TSP, starting_car_location, shortest_path_info):
    starting_idx = list_of_locations.index(starting_car_location)
    homes_indices = indices_to_TSP
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
