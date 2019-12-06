from generateOutput import *

def makeBetter(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy):
    # First check no-drive
    a, b, energy = dropAllAtSoda(list_locs, list_homes, start_car_loc, shortest_path_info)
    if energy < cur_energy:
        cur_a, cur_b, cur_energy = a, b, energy

    cur_a, cur_b, cur_energy = anneal(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy)
    return (cur_a, cur_b)
    

def anneal(list_locs, list_homes, start_car_loc, shortest_path_info, cur_a, cur_b, cur_energy, count=0):
    
    
    pass


def dropAllAtSoda(all_locs, homes, start_loc, shortest_path_info):
    car_route = [all_locs.index(start_loc)]
    return dropoffLocToOutput(car_route, shortest_path_info, homes, all_locs)



if __name__ == "__main__":
    anneal()