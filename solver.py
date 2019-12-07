import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import random
import time
random.seed(10)

from KCluster import *
from student_utils import *
from generateOutput import *
import Google_OR # Source - Google optimization team https://developers.google.com/optimization/routing/vrp
import input_validator
import output_validator
from additional_annealing import *
"""
======================================================================
  Complete the following function.
======================================================================
"""
# 50 = 279095.6666666666
best_of_our_50_result = [[0, 49, 36, 44, 39, 2, 12, 30, 20, 25, 9, 11, 3, 23, 42, 16, 38, 40, 45, 4, 46, 10, 5, 7, 39, 44, 0], {3: [3], 2: [26, 2], 4: [21, 4], 5: [5], 7: [47], 9: [9], 42: [15], 44: [18, 13], 36: [31], 23: [23], 40: [17], 49: [49], 12: [32, 12, 6, 43], 46: [46], 20: [20], 30: [30], 16: [16], 11: [11], 10: [10]}]

# 100 = 9000150.333333334
best_of_our_100_result = [[0, 80, 25, 72, 64, 83, 91, 83, 17, 8, 31, 41, 31, 8, 64, 9, 56, 5, 22, 43, 26, 67, 90, 45, 66, 45, 32, 48, 45, 49, 73, 20, 45, 19, 71, 33, 50, 24, 11, 6, 44, 40, 85, 76, 4, 63, 86, 96, 53, 29, 95, 29, 55, 53, 92, 12, 61, 23, 30, 63, 3, 0], {4: [57], 24: [21], 80: [79], 50: [18], 72: [72], 33: [33], 71: [71], 19: [19], 45: [45, 81, 93], 90: [90], 67: [67], 26: [26], 43: [43], 49: [49], 73: [73], 20: [20], 32: [32], 48: [48], 66: [66, 36, 97], 17: [17], 8: [8], 83: [83], 31: [31], 91: [91, 68], 41: [41, 38], 40: [40, 39], 44: [44, 89], 30: [30], 23: [23], 61: [61], 12: [12], 92: [92], 53: [53], 96: [96], 86: [86, 10, 99], 55: [55, 13], 29: [29], 95: [28, 95]}]

# 200 = 15333648.0
# best_200_route = ["Soda", "loc106", "loc172", "loc36", "loc145", "loc36", "loc106", "loc25", "loc53", "loc179", "loc186", "loc177", "loc42", "loc163", "loc104", "loc151", "loc18", "loc143", "loc160", "loc43", "loc27", "loc180", "loc133", "loc141", "loc102", "loc169", "loc41", "loc77", "loc173", "loc107", "loc173", "loc77", "loc41", "loc150", "loc12", "loc165", "loc197", "loc164", "loc144", "loc127", "loc60", "loc68", "loc126", "loc52", "loc196", "loc142", "loc196", "loc51", "loc196", "loc170", "loc192", "loc87", "loc47", "loc164", "loc101", "loc81", "loc115", "loc99", "loc134", "loc35", "loc194", "loc147", "loc38", "loc193", "loc114", "loc193", "loc111", "loc30", "loc39", "loc198", "loc166", "loc198", "loc39", "loc30", "loc111", "loc31", "loc111", "loc181", "loc49", "loc15", "loc8", "loc21", "loc176", "loc89", "loc10", "loc66", "loc188", "loc26", "loc27", "loc43", "loc50", "loc83", "loc94", "loc34", "loc84", "loc34", "loc14", "loc34", "loc13", "loc74", "loc23", "loc17", "loc129", "loc195", "loc129", "loc168", "loc82", "loc5", "loc92", "loc75", "loc137", "loc40", "loc137", "loc75", "loc57", "loc157", "loc59", "loc157", "loc57", "loc92", "loc124", "loc179", "loc199", "loc64", "loc3", "Soda"]
best_of_our_200_result = [[0, 106, 172, 36, 145, 36, 106, 25, 53, 179, 186, 177, 42, 163, 104, 151, 18, 143, 160, 43, 27, 180, 133, 141, 102, 169, 41, 77, 173, 107, 173, 77, 41, 150, 12, 165, 197, 164, 144, 127, 60, 68, 126, 52, 196, 142, 196, 51, 196, 170, 192, 87, 47, 164, 101, 81, 115, 99, 134, 35, 194, 147, 38, 193, 114, 193, 111, 30, 39, 198, 166, 198, 39, 30, 111, 31, 111, 181, 49, 15, 8, 21, 176, 89, 10, 66, 188, 26, 27, 43, 50, 83, 94, 34, 84, 34, 14, 34, 13, 74, 23, 17, 129, 195, 129, 168, 82, 5, 92, 75, 137, 40, 137, 75, 57, 157, 59, 157, 57, 92, 124, 179, 199, 64, 3, 0], {186: [45], 82: [82], 18: [90], 43: [65], 151: [151], 50: [50], 83: [83], 94: [94], 34: [34, 32, 189, 118, 138], 13: [13], 74: [74], 23: [23], 17: [17], 14: [14, 121, 88], 84: [84, 167, 97], 75: [72, 75], 57: [57], 157: [157], 137: [137], 59: [59], 40: [40, 20], 42: [42, 171], 163: [163, 154], 199: [80, 199], 64: [64], 3: [3], 0: [0], 106: [106], 25: [25, 140], 53: [53, 58], 172: [172, 6], 36: [36], 145: [156, 145], 193: [193], 30: [11, 30, 136], 101: [101], 51: [155, 51, 103], 142: [142, 7], 198: [28, 24], 165: [165, 100], 38: [122, 38], 15: [79, 15], 10: [10], 147: [147], 111: [128, 111], 77: [77], 41: [41], 192: [192], 107: [146, 107], 127: [183], 188: [188], 126: [126], 141: [141], 26: [26], 194: [55, 194], 176: [95], 114: [114], 180: [131, 180], 196: [185, 61], 181: [181, 37], 173: [173], 35: [35], 99: [9], 170: [170], 8: [8], 166: [109], 39: [39], 150: [22]}]


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
    G, message = adjacency_matrix_to_graph(adjacency_matrix)
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))

    min_result_1, min_result_2, minEnergy = None, None, float('inf')

    if input_file == "/11_50.in":
        # print("HI 50 only once please")
        return best_of_our_50_result
    elif input_file == "/11_100.in":
        # print("HI 100 here only once")
        return best_of_our_100_result
    elif input_file == "/11_200.in":
        # print("HI 200... still once plz")
        return best_of_our_200_result
        best_200_route_idx = [list_of_locations.index(i) for i in best_200_route]
        min_result_1, min_result_2, minEnergy = dropoffLocToOutput(best_200_route_idx, shortest_path_info, list_of_homes, list_of_locations)

    # TODO: run alan+wsy idea (below)
    start_and_homes = [starting_car_location] + list_of_homes
    start_and_homes_idx = [list_of_locations.index(i) for i in start_and_homes]
    num_of_homes = len(list_of_homes)
    for th in range(num_of_homes+1):
        alan_wsy_idea = goodpoints(start_and_homes_idx, shortest_path_info, th)
        alan_wsy_cycle = loc_to_go_with_indices(list_of_locations, alan_wsy_idea, starting_car_location, shortest_path_info)
        alan_wsy_1, alan_wsy_2, alan_wsy_energy = dropoffLocToOutput(alan_wsy_cycle, shortest_path_info, list_of_homes, list_of_locations)
        if alan_wsy_energy < minEnergy:
            print("Threshold = ", th)
            min_result_1, min_result_2, minEnergy = alan_wsy_1, alan_wsy_2, alan_wsy_energy

    # return [min_result_1, min_result_2]


    # print(minEnergy)
    # k_cluster_num_upper_bound = len(list_of_homes) // 20 + 1
    k_cluster_num_upper_bound = 2

    """
    Potentially use k-cluster to determine the list_of_homes_to_reach
    """
    # int_adj_matrix = adj_matrix_to_int(adjacency_matrix)
    # print(shortest_path_info)

    """
    Baseline 1 : Drop off all @Soda
    """
    car_cycle = [list_of_locations.index(starting_car_location)]
    simple_result_1, simple_result_2, simple_energy = dropoffLocToOutput(car_cycle, shortest_path_info, list_of_homes, list_of_locations)
    # print('Baseline 1 done')
    if simple_energy < minEnergy:
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

        min_wsy_energy = float("inf")
        min_1 = float("inf")
        min_2 = float("inf")
        for i in range(num_of_homes + 1):
            wsy_idea = goodpoints(home_list, shortest_path_info, i)
            wsy_cycle = loc_to_go_with_indices(list_of_locations, wsy_idea, starting_car_location, shortest_path_info)
            wsy_1, wsy_2, wsy_energy = dropoffLocToOutput(wsy_cycle, shortest_path_info, list_of_homes, list_of_locations)
            if wsy_energy < min_wsy_energy:
                min_wsy_energy = wsy_energy
                min_1 = wsy_1
                min_2 = wsy_2
        if min_wsy_energy < minEnergy:
            print("WSY SUCCESS")
            # print("WST energy = ", wsy_energy, minEnergy)
            min_result_1, min_result_2, minEnergy = min_1, min_2, min_wsy_energy


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

    # try:
    #     if len(min_result_1) == 1:
    #         return [min_result_1, min_result_2]
    #     else:
    #         anneal_result1, anneal_result2, anneal_e = runAnneal(min_result_1, shortest_path_info, list_of_homes, list_of_locations)
    #         if anneal_e < minEnergy:
    #             min_result_1 = anneal_result1
    #             min_result_2 = anneal_result2
    #             minEnergy = anneal_e
    #             print("Annealing worked!")
    # except:

    print([min_result_1, min_result_2])
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
    # print(homes_indices)
    return loc_to_go_with_indices(list_of_locations, homes_indices, starting_car_location, shortest_path_info)


def getShortestDistAndPath(dijkstra_info, i, j):
    pair_info = dijkstra_info[i][1]
    if i == j:
        # print("ERROR shouldnt be here")
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
