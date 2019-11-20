# project-fa19
CS 170 Fall 2019 Project
# 170-Project

注：目前仅支持TSP over the entire graph
# 需改进：
1. modify TSP to cover at least just the list_of_homes
2. allow multiple enterings of same location --> 例子，一张条线（可以做edge case！一张条线 + 一个特别长的edge返回原点, i.e. Start --1-- A --1-- B --1-- C --1000-- Start

Update on how to use my system:
Change params at the top of generateInput.py --> run in command line: python3 generateInput.py
Copy the entire result into a xxx.in file (请自行命名)
To run the solver, type in command line: python3 solver.py xxx.in xxx.out
e.g. running "python3 solver.py 200.in 200.out" currently would print:
Processing 200.in
Total energy =  760.0  with driving energy =  760.0  and walking energy =  0

Time taken is < 10 seconds

# TODO
0. All : come up with edge cases + 最好能有easily加进一个generated random graph的方式
1. Rui : think about the two modifications listed above OR try your own method (public libraries etc)
2. Shunyu : k-clustering --> also a potential improvement to the current TSP-solver
3. Alan : similar to Rui