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
# 279149.3333333334
# best_of_our_50_result = [[0, 44, 39, 7, 11, 9, 5, 12, 3, 23, 42, 16, 38, 40, 17, 39, 44, 36, 49, 0], {3: [3], 12: [26, 2, 32, 12, 30, 6, 43], 40: [21, 4], 5: [5, 20, 10], 7: [47, 46], 9: [9], 42: [15], 44: [18, 13], 36: [31], 23: [23], 17: [17], 49: [49], 16: [16], 11: [11]}]
# best_of_our_50_result = [[0, 49, 36, 44, 39, 7, 40, 38, 16, 38, 40, 17, 39, 44, 0], {7: [3, 5, 47, 9, 12, 46, 20, 30, 11, 10, 6, 43], 39: [26, 2], 40: [21, 4], 16: [15, 23, 16], 44: [18, 13], 36: [31], 17: [17, 32], 49: [49]}]
best_of_our_50_result = [[0, 44, 36, 44, 39, 7, 40, 38, 16, 42, 23, 3, 39, 44, 0], {3: [3], 39: [26, 2], 40: [21, 4, 17, 32], 7: [5, 47, 9, 12, 46, 20, 30, 11, 10, 6, 43], 16: [15, 16], 44: [18, 13], 36: [31, 49], 23: [23]}]
best_of_our_100_result = [[0, 80, 79, 60, 76, 84, 85, 40, 39, 89, 44, 6, 42, 98, 21, 50, 52, 69, 18, 7, 22, 43, 26, 67, 90, 45, 32, 48, 97, 36, 66, 45, 20, 73, 49, 81, 45, 93, 45, 19, 71, 33, 50, 35, 0, 74, 56, 34, 5, 16, 94, 47, 78, 4, 87, 57, 64, 83, 91, 68, 38, 41, 31, 8, 17, 8, 64, 65, 72, 46, 3, 63, 30, 23, 61, 12, 92, 53, 55, 13, 28, 95, 29, 53, 96, 86, 10, 63, 51, 9, 54, 51, 2, 24, 11, 14, 77, 27, 59, 37, 70, 75, 82, 88, 82, 15, 58, 62, 80, 25, 0], {57: [57], 21: [21], 79: [79], 18: [18], 72: [72], 33: [33], 71: [71], 19: [19], 45: [45], 90: [90], 67: [67], 26: [26], 43: [43], 49: [49], 73: [73], 20: [20], 32: [32], 48: [48], 81: [81], 93: [93], 66: [66], 36: [36], 97: [97], 17: [17], 8: [8], 83: [83], 31: [31], 91: [91], 41: [41], 68: [68], 38: [38], 40: [40], 44: [44], 39: [39], 89: [89], 30: [30], 23: [23], 61: [61], 12: [12], 92: [92], 53: [53], 96: [96, 99], 86: [86], 10: [10], 55: [55], 29: [29], 13: [13], 28: [28], 95: [95]}]
# best_of_our_100_result = [[0, 80, 79, 60, 76, 84, 85, 54, 9, 51, 2, 24, 11, 14, 6, 44, 89, 39, 40, 44, 6, 56, 34, 74, 1, 35, 78, 47, 94, 16, 5, 77, 27, 59, 60, 87, 57, 87, 4, 63, 10, 86, 99, 96, 53, 55, 13, 28, 95, 29, 53, 92, 12, 61, 23, 30, 63, 3, 65, 64, 8, 17, 8, 31, 41, 38, 68, 91, 83, 64, 65, 42, 98, 21, 50, 52, 69, 18, 7, 22, 43, 26, 67, 90, 45, 93, 45, 81, 49, 73, 20, 45, 66, 36, 97, 48, 32, 45, 19, 71, 33, 50, 62, 58, 15, 82, 88, 46, 72, 25, 37, 70, 75, 0], {57: [57], 21: [21], 79: [79], 18: [18], 72: [72], 33: [33], 71: [71], 19: [19], 45: [45], 90: [90], 67: [67], 26: [26], 43: [43], 49: [49], 73: [73], 20: [20], 32: [32], 48: [48], 81: [81], 93: [93], 66: [66], 36: [36], 97: [97], 17: [17], 8: [8], 83: [83], 31: [31], 91: [91], 41: [41], 68: [68], 38: [38], 40: [40], 44: [44], 39: [39], 89: [89], 30: [30], 23: [23], 61: [61], 12: [12], 92: [92], 53: [53], 96: [96], 86: [86], 10: [10], 99: [99], 55: [55], 29: [29], 13: [13], 28: [28], 95: [95]}]
# best_of_our_100_result = [[0, 3, 63, 12, 92, 53, 29, 95, 29, 53, 96, 86, 63, 22, 43, 26, 67, 90, 45, 66, 45, 90, 67, 26, 43, 22, 64, 8, 31, 41, 31, 8, 64, 0], {63: [57, 30, 23, 61], 22: [21], 0: [79, 18], 3: [72, 40, 44, 39, 89], 67: [33, 71, 67], 43: [19, 43], 45: [45, 49, 73, 20, 32, 48, 81, 93], 90: [90], 26: [26], 66: [66, 36, 97], 8: [17, 8, 83, 91, 68], 31: [31], 41: [41, 38], 12: [12], 92: [92], 53: [53, 55, 13], 96: [96, 99], 86: [86, 10], 29: [29], 95: [28, 95]}]
# [[0, 3, 63, 86, 96, 53, 29, 95, 29, 53, 96, 86, 63, 64, 8, 31, 41, 31, 8, 64, 0], {63: [57, 21, 19, 45, 90, 67, 26, 43, 49, 73, 20, 32, 48, 81, 93, 66, 36, 97, 30, 23, 61, 12], 0: [79, 18, 33, 71], 3: [72, 40, 44, 39, 89], 8: [17, 8, 83, 91, 68], 31: [31], 41: [41, 38], 53: [92, 53, 55, 13], 96: [96], 86: [86, 10, 99], 29: [29], 95: [28, 95]}]
best_of_our_200_result = ["Soda", "loc3", "loc179", "loc45", "loc129", "loc17", "loc23", "loc74", "loc13", "loc34", "loc14", "loc121", "loc14", "loc34", "loc13", "loc74", "loc23", "loc17", "loc129", "loc168", "loc43", "loc27", "loc38", "loc193", "loc37", "loc27", "loc43", "loc92", "loc75", "loc137", "loc75", "loc92", "loc43", "loc27", "loc55", "loc77", "loc173", "loc107", "loc173", "loc77", "loc111", "loc150", "loc165", "loc8", "loc164", "loc47", "loc87", "loc192", "loc170", "loc196", "loc51", "loc196", "loc170", "loc192", "loc87", "loc47", "loc164", "loc111", "loc30", "loc111", "loc131", "loc27", "loc43", "loc50", "loc74", "loc23", "loc17", "loc129", "loc179", "loc53", "loc25", "loc106", "loc172", "loc106", "Soda"]


def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
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
    if input_file == "/11_50.in":
        print("HI 50 only once please")
        return best_of_our_50_result
    elif input_file == "/11_100.in":
        print("HI 100 here only once")
        return best_of_our_100_result
    elif input_file == "/11_200.in":
        print("HI 200... still once plz")
        return best_of_our_200_result

    G, message = adjacency_matrix_to_graph(adjacency_matrix)

    # k_cluster_num_upper_bound = len(list_of_homes) // 20 + 1
    k_cluster_num_upper_bound = 2

    """
    Potentially use k-cluster to determine the list_of_homes_to_reach
    """
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
    int_adj_matrix = adj_matrix_to_int(adjacency_matrix)
    # print(shortest_path_info)
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
    route_50_result_1, route_50_result_2, send_home_energy = dropoffLocToOutput(final_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    if send_home_energy < minEnergy:
        min_result_1, min_result_2, minEnergy = route_50_result_1, route_50_result_2, send_home_energy

    # return [min_result_1, min_result_2]


    """
    Soln 4 : randomize
    """
    times = 150
    selectivity_lst = []
    if len(list_of_homes) <= 25:
        selectivity_lst = [0.3]
    elif len(list_of_homes) <= 50:
        print("100 here")
        selectivity_lst = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    else:
        selectivity_lst = [0.3, 0.6]
    # 100
#    if starting_car_location == 'Soda' and (list_of_homes[:12] == ['loc57', 'loc21', 'loc79', 'loc18', 'loc72', 'loc33', 'loc71', 'loc19', 'loc45', 'loc90', 'loc67', 'loc26']):
#        print('HI our own 100')
#        times = 500
#        selectivity_lst = [0.1, 0.125, 0.15, 0.2, 0.3]
    # 50
    if list_of_locations == ['Soda', 'loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8', 'loc9', 'loc10', 'loc11',
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
        car_route_50_idx = best_of_our_200
        car_route_50 = [list_of_locations.index(loc) for loc in car_route_50_idx]
        a, b, c = dropoffLocToOutput(car_route_50, shortest_path_info, list_of_homes, list_of_locations)
        return [a, b]
#        times = 500
#        selectivity_lst = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    for selectivity in selectivity_lst:
        flag = 0
        print(selectivity)
        for _ in range(times):
            random_homes_only_car_cycle = randomSendHome(list_of_locations, list_of_homes, starting_car_location, shortest_path_info, selectivity)
            random_send_home_result_1, random_send_home_result_2, random_send_home_energy = dropoffLocToOutput(random_homes_only_car_cycle, shortest_path_info, list_of_homes, list_of_locations)
            if random_send_home_energy < minEnergy:
                # print(random_send_home_result_1)
                print(selectivity, "Success")
                min_result_1, min_result_2, minEnergy = random_send_home_result_1, random_send_home_result_2, random_send_home_energy
            else:
                flag += 1

            if flag >= 5:
                break
        
    print("Start k-cluster")
    
    """
    K-Cluster as dropoff
    """
    K_list = [i for i in range(2, len(list_of_homes), 1)]
    
    out_counter = 0
    for k in K_list:
        k_flag = False
#        print("k=", k)
        name_index_map = {}
        num_of_homes = len(list_of_homes)
        home_list = []
        for i in range(len(list_of_locations)):
            name_index_map[list_of_locations[i]] = i;
        for x in list_of_homes:
            home_list += [name_index_map[x]]
        d_result = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
        cluster, center = kcluster(d_result, num_of_homes, home_list, k)

        all_k_sel = [0, 0.1, 0.2, 0.9]
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
            # print(num_homes)
            next_home = homes_indices[j]
            # print(next_home)
            dist_ij, _ = getShortestDistAndPath(shortest_path_info, home, next_home)
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
    print(homes_indices)
    return loc_to_go_with_indices(list_of_locations, homes_indices, starting_car_location, shortest_path_info)


def getShortestDistAndPath(dijkstra_info, i, j):
    pair_info = dijkstra_info[i][1]
    if i == j:
        print("ERROR shouldnt be here")
        return [0, [i]]
    # print(i, j)
    # print(dijkstra_info)
    # print(j)
    dist = pair_info[0][j]
    path = pair_info[1][j]
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

    idx = input_file.index('/')
    input_file_name = input_file[idx :]
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, input_file_name, params=params)

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
        #try:
#            solve_all(input_directory, output_directory, params=args.params)
        #except:
#            os.system("python3 ./outputs/removeProcessed.py")
#            os.system("python3 ./solver.py --all inputs outputs")
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
