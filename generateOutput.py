"""
@input
    car_route = list of places the car would go to (first = starting_car_location, last = starting_car_location)
    shortest_path_info = result of shortest_paths_and_lengths (dijkstra from nx library)
    list_of_homes, list_of_locs = input directly from solver#solve
@output - a list of 3 things
    1st and 2nd = result needed for output
    3rd = total energy expenditure (need minimize, stored for self-reference)
"""
def dropoffLocToOutput(car_route, shortest_path_info, list_of_homes, list_of_locs):
    dropoff_info = {}
    walking_dist = 0
    driving_dist = 0

    for home in list_of_homes:
        home_idx = list_of_locs.index(home)
        distDict = shortest_path_info[home_idx][1][0]
        
        minDropoff = min(car_route, key=lambda loc: distDict[loc])
        if minDropoff in dropoff_info.keys():
            dropoff_info[minDropoff].append(home)
        else:
            dropoff_info[minDropoff] = [home]

        minDist = distDict[minDropoff]
        walking_dist += minDist

    for idx in range(len(car_route) - 1):
        loc, next_loc = car_route[idx], car_route[idx + 1]
        loc_idx = list_of_locs.index(loc)
        loc_dist_dict = shortest_path_info[home_idx][1][0]
        driving_dist += loc_dist_dict[next_loc]

    total_energy = driving_dist * 2.0 / 3.0 + walking_dist

    dropoff_result = list(dropoff_info)
    for idx in range(len(dropoff_result)):
        single_dropoff_loc = dropoff_result[idx]
        dropoff_result[idx] = [single_dropoff_loc, dropoff_info[single_dropoff_loc]]

    return [car_route, dropoff_result, total_energy]
