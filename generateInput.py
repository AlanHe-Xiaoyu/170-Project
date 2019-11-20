"""
s - 2k
"""
size = 50
connectivity = 0.7


print(size)
print(size // 2)

print('Soda ' + ' '.join(["loc" + str(i) for i in range(size - 1)]))
print(' '.join(["loc" + str(i) for i in range(0, size - 1, 2)]))
print('Soda')

adj_matrix = []
for i in range(size):
    adj_matrix.append(['x'] * size)

import numpy as np
for i in range(size):
    for j in range(size):
        if i > j:
            sample = np.random.random()
            if sample > (1 - connectivity): # add edge
                resample = str(int(np.random.random() * 25) + int(np.random.random() * 50))
                adj_matrix[i][j] = resample
                adj_matrix[j][i] = resample

for i in range(size):
    print(' '.join(adj_matrix[i]))

# int_adj_matrix = []
# for i in range(size):
#     curRow = []
#     for j in range(size):
#         dist = adj_matrix[i][j]
#         if dist == 'x':
#             curRow.append(100000)
#         else:
#             curRow.append(int(dist))
#     int_adj_matrix.append(curRow)

# print(int_adj_matrix)