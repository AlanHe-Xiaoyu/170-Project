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

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
    G, message = adjacency_matrix_to_graph(adjacency_matrix)
    shortest_path_info = list(shortest_paths_and_lengths(list_of_locations, adjacency_matrix))
    min_result_1, min_result_2, minEnergy = None, None, float('inf')

    start_and_homes = [starting_car_location] + list_of_homes
    start_and_homes_idx = [list_of_locations.index(i) for i in start_and_homes]

    for th in [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]:
        alan_wsy_idea = goodpoints(start_and_homes_idx, shortest_path_info, th)
        alan_wsy_cycle = loc_to_go_with_indices(list_of_locations, alan_wsy_idea, starting_car_location, shortest_path_info)
        alan_wsy_1, alan_wsy_2, alan_wsy_energy = dropoffLocToOutput(alan_wsy_cycle, shortest_path_info, list_of_homes, list_of_locations)
        if alan_wsy_energy < minEnergy:
            print("Threshold = ", th)
            min_result_1, min_result_2, minEnergy = alan_wsy_1, alan_wsy_2, alan_wsy_energy

    return [min_result_1, min_result_2]




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
