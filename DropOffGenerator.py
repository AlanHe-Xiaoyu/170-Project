import networkx as nx
import numpy as np
import random
def DropOffGenerator(adjacency_matrix, number_of_houses, number_of_locations):
    set_of_dropoff = []
    for i in range(number_of_houses):
        x = random.randrange(0, number_of_locations, 1)
        set_of_dropoff = set_of_dropoff + [x]
    return set_of_dropoff