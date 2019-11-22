"""
s - 2k
"""
import solver, os

def startGen():
    fileName = '50_prep_30.in'
    size = 30
    connectivity = 0.7
    edge_weight_cap = 30
    
    f = open(fileName,"w+")
    f.write(str(size)+os.linesep)
    f.write(str(size // 2)+os.linesep)

    all_locs =["Soda"] + ["loc" + str(i) for i in range(size - 1)]
    location_map = {}
    for i in range(len(all_locs)):
        location_map[all_locs[i]] = i
    f.write('Soda ' + ' '.join(["loc" + str(i) for i in range(size - 1)])+os.linesep)
    f.write(' '.join(["loc" + str(i) for i in range(0, size - 1, 2)])+os.linesep)
    f.write('Soda'+os.linesep)

    adj_matrix = []
    for i in range(size):
        adj_matrix.append(['x'] * size)

    import numpy as np
    for i in range(size):
        for j in range(size):
            if i > j:
                sample = np.random.random()
                if sample > (1 - connectivity): # add edge
                    resample = int(np.random.random() * edge_weight_cap)
                    while resample == 0:
                        resample = int(np.random.random() * edge_weight_cap)
                    adj_matrix[i][j] = resample
                    adj_matrix[j][i] = resample


    changed = True
    while changed:
        changed = False
        dijkstra_result = solver.shortest_paths_and_lengths(all_locs, adj_matrix)
        dijkstra_info = list(dijkstra_result)
        for node, (dist, path) in dijkstra_info:
            for dest in range(size):
                if dest not in dist:
                    length = int(np.random.random() * 25) + int(np.random.random() * 50)
                    adj_matrix[node][dest] = length
                    adj_matrix[dest][node] = length
                    changed = True
                else:
                    if (adj_matrix[node][dest] is not 'x') and (dist[dest] < adj_matrix[node][dest]):
                        adj_matrix[node][dest] = dist[dest]
                        adj_matrix[dest][node] = dist[dest]
                        changed = True

    for i in range(size):
        for j in range(size):
            adj_matrix[i][j] = str(adj_matrix[i][j])
    for i in range(size):
        f.write(' '.join(adj_matrix[i]) + os.linesep)


if __name__ == '__main__':
    startGen()