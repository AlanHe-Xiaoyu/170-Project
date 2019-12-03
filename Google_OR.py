""" Source - Google optimization team https://developers.google.com/optimization/routing/vrp """

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    """ 20 points """
    # data['distance_matrix'] = [[100000, 100000, 100000, 17, 100000, 100000, 41, 8, 49, 59, 100000, 49, 58, 17, 100000, 9, 61, 36, 41, 51], [100000, 100000, 9, 100000, 37, 37, 16, 61, 35, 38, 50, 35, 51, 16, 23, 20, 9, 27, 47, 19], [100000, 9, 100000, 100000, 54, 49, 16, 46, 43, 100000, 100000, 57, 100000, 28, 100000, 100000, 40, 31, 44, 51], [17, 100000, 100000, 100000, 23, 71, 61, 41, 100000, 62, 100000, 20, 35, 100000, 34, 100000, 64, 100000, 100000, 51], [100000, 37, 54, 23, 100000, 57, 100000, 56, 41, 36, 100000, 33, 24, 54, 16, 100000, 47, 47, 19, 13], [100000, 37, 49, 71, 57, 100000, 41, 100000, 100000, 33, 100000, 71, 26, 53, 29, 15, 31, 48, 100000, 27], [41, 16, 16, 61, 100000, 41, 100000, 100000, 54, 28, 15, 100000, 45, 100000, 100000, 27, 54, 56, 18, 100000], [8, 61, 46, 41, 56, 100000, 100000, 100000, 100000, 51, 30, 100000, 100000, 52, 38, 17, 27, 44, 100000, 100000], [49, 35, 43, 100000, 41, 100000, 54, 100000, 100000, 100000, 14, 5, 60, 100000, 37, 7, 41, 51, 23, 17], [59, 38, 100000, 62, 36, 33, 28, 51, 100000, 100000, 100000, 46, 100000, 100000, 100000, 72, 50, 100000, 100000, 52], [100000, 50, 100000, 100000, 100000, 100000, 15, 30, 14, 100000, 100000, 44, 45, 100000, 10, 14, 100000, 18, 38, 58], [49, 35, 57, 20, 33, 71, 100000, 100000, 5, 46, 44, 100000, 100000, 100000, 11, 25, 31, 100000, 12, 50], [58, 51, 100000, 35, 24, 26, 45, 100000, 60, 100000, 45, 100000, 100000, 61, 29, 100000, 32, 13, 49, 100000], [17, 16, 28, 100000, 54, 53, 100000, 52, 100000, 100000, 100000, 100000, 61, 100000, 67, 49, 54, 22, 22, 100000], [100000, 23, 100000, 34, 16, 29, 100000, 38, 37, 100000, 10, 11, 29, 67, 100000, 100000, 100000, 37, 9, 53], [9, 20, 100000, 100000, 100000, 15, 27, 17, 7, 72, 14, 25, 100000, 49, 100000, 100000, 44, 100000, 12, 43], [61, 9, 40, 64, 47, 31, 54, 27, 41, 50, 100000, 31, 32, 54, 100000, 44, 100000, 43, 100000, 19], [36, 27, 31, 100000, 47, 48, 56, 44, 51, 100000, 18, 100000, 13, 22, 37, 100000, 43, 100000, 41, 23], [41, 47, 44, 100000, 19, 100000, 18, 100000, 23, 100000, 38, 12, 49, 22, 9, 12, 100000, 41, 100000, 36], [51, 19, 51, 51, 13, 27, 100000, 100000, 17, 52, 58, 50, 100000, 100000, 53, 43, 19, 23, 36, 100000]]    
    # data['num_vehicles'] = 1
    data['depot'] = 0
    return data

# def print_solution(data, manager, routing, solution):
#     """Prints solution on console."""
#     max_route_distance = 0
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
#         route_distance = 0
#         while not routing.IsEnd(index):
#             plan_output += ' {} -> '.format(manager.IndexToNode(index))
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             route_distance += routing.GetArcCostForVehicle(
#                 previous_index, index, vehicle_id)
#         plan_output += '{}\n'.format(manager.IndexToNode(index))
#         plan_output += 'Distance of the route: {}m\n'.format(route_distance)
#         print(plan_output)
#         max_route_distance = max(route_distance, max_route_distance)
#     print('Maximum of the route distances: {}m'.format(max_route_distance))


def print_solution(data, manager, routing, assignment):
    car_route = []
    """
    for vehicle_id in range(data['num_vehicles']):
        index = 0
        while not routing.IsEnd(index):
            car_route.append(index)
            index = assignment.Value(routing.NextVar(index))
        car_route.append(0)
    return car_route
    """

    # dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        # if assignment.Value(routing.NextVar(node)) == node:
            # dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    # print(dropped_nodes)
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        # print(index)
        while not routing.IsEnd(index):
            car_route.append(index)

            node_index = manager.IndexToNode(index)
            index = assignment.Value(routing.NextVar(index))
        car_route.append(0)

    # print('Total Distance of all routes: {}m'.format(total_distance))
    # print('Total Load of all routes: {}'.format(total_load))

    return car_route



def main_func(adj_matrix, num_vehicles):
    # Instantiate the data problem.
    data = create_data_model()
    data['distance_matrix'] = adj_matrix
    data['num_vehicles'] = num_vehicles

    # data['demands'] = [0] + [1 for _ in range(len(adj_matrix) - 1)]
    # data['vehicle_capacities'] = [200 for _ in range(num_vehicles)]
    # data['starts'] = [0 for _ in range(num_vehicles)]
    # data['ends'] = [0 for _ in range(num_vehicles)]
    # print(data['starts'], data['ends'])

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        return print_solution(data, manager, routing, assignment)
    else:
        return None


if __name__ == '__main__':
    main_func([], 1)