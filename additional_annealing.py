from generateOutput import *
# from solver import *
from simanneal import Annealer
import random
import numpy as np
import os
import sys

from KCluster import *
from student_utils import *
from generateOutput import *
import Google_OR # Source - Google optimization team https://developers.google.com/optimization/routing/vrp
import input_validator
import output_validator

class DTHProblem(Annealer):
    """Test annealer with a travelling salesman problem."""
    def __init__(self, initialList, shortest_path_info, list_of_homes, list_of_locs):
        print(initialList)
        self.shortest_path_info = shortest_path_info
        self.list_of_homes = list_of_homes
        self.list_of_locs = list(range(len(list_of_locs))) #index
        self.original_loc = list_of_locs #name
        super(DTHProblem, self).__init__(initialList)
        self.minE = 279097
    def move(self):
        initial_energy = self.energy()
        """ 0 - add, 1-remove, 2-randomly swap"""
        add_weight = 1.0
        remove_weight = 1.0
        swap_weight = 1.0
        weights = []
        choices = []
        
        not_included = []
        for i in self.list_of_locs:
            if i not in self.state:
                not_included.append(i)
        if len(not_included) == 0:
            choices = [1]
            weights = [remove_weight, swap_weight]
        elif len(self.state) <= 3:
            choices = [0]
            weights = [1.0]
        else:
            if len(self.state) > 2:
                choices = [0,1]
                weights = [add_weight, remove_weight]
            else:
                choices = [0]
                weights = [add_weight]
        method = np.random.choice(choices)
        if method == 2:
            a = random.randint(1, len(self.state) - 1)
            b = random.randint(1, len(self.state) - 1)
            self.state[a], self.state[b] = self.state[b], self.state[a]
        elif method == 1:
            if len(self.state) <= 2:
                a = 0
            else:
                a = random.randint(1, len(self.state) - 1)
            self.state.pop(a)
        else:
            a = random.choice(not_included)
            self.state.append(a)
        return self.energy() - initial_energy
        
    def energy(self):
#    def loc_to_go_with_indices(list_of_locations, indices_to_TSP, starting_car_location, shortest_path_info):
        actual_route = annealing_full_path(self.original_loc, self.state, self.shortest_path_info)
        a, b, ennn = dropoffLocToOutput(actual_route, self.shortest_path_info, self.list_of_homes, self.original_loc)
        if ennn < self.minE:
            print([ennn,a,b])
            self.minE = ennn
        return ennn
        
def runAnneal(initialList, shortest_path_info, list_of_homes, list_of_locs):
    print("Start annealing")
    tsp = DTHProblem(initialList, shortest_path_info, list_of_homes, list_of_locs)
    tsp.set_schedule(tsp.auto(minutes=0.0002))
    tsp.copy_strategy = "slice"
    res, e = tsp.anneal()
    res1, res2, en = dropoffLocToOutput(res, shortest_path_info, list_of_homes, list_of_locs)
    return res1, res2, en
#def makeBetter(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy):
#    # First check no-drive
#    a, b, energy = dropAllAtSoda(list_locs, list_homes, start_car_loc, shortest_path_info)
#    if energy < cur_energy:
#        cur_a, cur_b, cur_energy = a, b, energy
#
#    cur_a, cur_b, cur_energy = anneal(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy)
#    return (cur_a, cur_b)
#
#
#def anneal(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy, count=0):
#
#
#    pass

"""
Helpers
"""
def annealing_full_path(list_of_locations, indices_to_TSP, shortest_path_info):
#    starting_idx = list_of_locations.index(starting_car_location)
    homes_indices = indices_to_TSP
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


def dropAllAtSoda(all_locs, homes, start_loc, shortest_path_info):
    car_route = [all_locs.index(start_loc)]
    return dropoffLocToOutput(car_route, shortest_path_info, homes, all_locs)

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

if __name__ == "__main__":
    anneal()
