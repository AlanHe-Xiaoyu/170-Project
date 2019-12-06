from generateOutput import *
from solver import *
from simanneal import Annealer
import random
import numpy as np
class DTHProblem(Annealer):
    """Test annealer with a travelling salesman problem."""
    def __init__(self, initialList, shortest_path_info, list_of_homes, list_of_locs):
        print(initialList)
        self.shortest_path_info = shortest_path_info
        self.list_of_homes = list_of_homes
        self.list_of_locs = list(range(len(list_of_locs))) #index
        self.original_loc = list_of_locs #name
        super(DTHProblem, self).__init__(initialList)
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
            choices = [1,2]
            weights = [remove_weight, swap_weight]
        elif len(self.state) == 0:
            choices = [0]
            weights = [1.0]
        else:
            if len(self.state) > 2:
                choices = [0,1,2]
                weights = [add_weight, remove_weight, swap_weight]
            else:
                choices = [0]
                weights = [add_weight]
        method = np.random.choice(choices)
        if method == 2:
             g = 1+1
#            a = random.randint(1, len(self.state) - 2)
#            b = random.randint(1, len(self.state) - 2)
#            self.state[a], self.state[b] = self.state[b], self.state[a]
        elif method == 1:
            a = random.randint(1, len(self.state) - 2)
            path_to_add = getShortestDistAndPath(self.shortest_path_info, self.state[a-1], self.state[a+1])[1]
            path_to_add = path_to_add[1:-1]
            self.state.pop(a)
            self.state[a:a] = path_to_add
        else:
            a = random.choice(not_included)
            b = random.randint(1, len(self.state) - 2)
            path_before_a = getShortestDistAndPath(self.shortest_path_info, self.state[b-1], a)[1]
            path_before_a = path_before_a[1:]
            path_after_a = getShortestDistAndPath(self.shortest_path_info, a, self.state[b+1])[1]
            added_path = path_before_a + path_after_a[1:-1]
            self.state[b:b] = added_path
        return self.energy() - initial_energy
        
    def energy(self):
        _, __, ennn = dropoffLocToOutput(self.state, self.shortest_path_info, self.list_of_homes, self.original_loc)
        return ennn
        
def runAnneal(initialList, shortest_path_info, list_of_homes, list_of_locs):
    print("Start annealing")
    tsp = DTHProblem(initialList, shortest_path_info, list_of_homes, list_of_locs)
    tsp.set_schedule(tsp.auto(minutes=0.2))
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


def dropAllAtSoda(all_locs, homes, start_loc, shortest_path_info):
    car_route = [all_locs.index(start_loc)]
    return dropoffLocToOutput(car_route, shortest_path_info, homes, all_locs)



if __name__ == "__main__":
    anneal()
