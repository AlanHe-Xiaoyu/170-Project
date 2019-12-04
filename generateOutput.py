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
    # print(car_route)
    dropoff_info = {}
    walking_dist = 0
    driving_dist = getDrivingDist(car_route, shortest_path_info)

    for home in list_of_homes:
        home_idx = list_of_locs.index(home)
        home = list_of_locs[home_idx]
        distDict = shortest_path_info[home_idx][1][0]
        
        minDropoff = min(car_route, default=0, key=lambda loc: distDict[loc])
        if minDropoff in dropoff_info.keys():
            dropoff_info[minDropoff].append(home_idx)
        else:
            dropoff_info[minDropoff] = [home_idx]

        minDist = distDict[minDropoff]
        walking_dist += minDist

    total_energy = driving_dist * 2.0 / 3.0 + walking_dist
    # print(car_route)
    return [car_route, dropoff_info, total_energy]


def getDrivingDist(car_route, shortest_path_info):
    total_driving_cost = 0

    for i in range(len(car_route) - 1):
        loc_idx, next_loc_idx = car_route[i], car_route[i + 1]
        # print(loc_idx, next_loc_idx)
        loc_dist_dict = shortest_path_info[loc_idx][1][0]
        total_driving_cost += loc_dist_dict[next_loc_idx]

    return total_driving_cost