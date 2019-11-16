import numpy as np
import matplotlib.pyplot as plt
import copy

# MCMC (Simulated Annealing) solution for Traveling Salesman problem
# start from city 1 to city N

N = 20 # the number of cities

# simulate a distance matrix
distance = np.random.rand(N, N)
distance = (distance + distance.T) / 2.0
ind_diag = range(N)
distance[ind_diag, ind_diag] = 0

# Calculate total distance for a given sequence
def cal_dist(distance, L):
    d = 0
    for i in range(len(L)):
        d = d + distance[L[i % N], L[(i + 1) % N]]
    return d

T = float(pow(2, -8)) # free parameters, inversely related to the probability of rejection if the direction is wrong

ITER = 10000
L = np.arange(N) # initail route sequence
print (cal_dist(distance, L)) # initial distance
dist_all = []
for i in range(ITER):
    a = np.random.randint(1, N - 1)
    d_t = cal_dist(distance, L)
    dist_all.append(d_t)
    L_tmp = copy.copy(L)
    L_tmp[[a, (a + 1)%N]] = L_tmp[[(a + 1)%N, a]]
    delta_d = cal_dist(distance, L_tmp) - d_t
    p = min(1, np.exp(-1 * delta_d / T))
    u = np.random.rand()
    if u < p:
        L = L_tmp

print (cal_dist(distance, L)) # final distance
plt.plot(dist_all)