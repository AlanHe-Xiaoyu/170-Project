# project-fa19
CS 170 Fall 2019 Project
# 170-Project

50 location name mapping : 
50 pre-randomized solution :
- Gadget1 Loop : (0) -- 30~34 -- (21)
    Should do (0) -- 30 -- 31 -- 30 -- (0) + (21) -- 34 -- 33 -- 34 -- (21) with 32 dropoff @31/32 --> cost = car 1348 + walk 1000
- Gadget2 Star : (10) -- 35~45
    Should do (10) -- 35 -- 36 -- 37 -- 35 -- 40 -- 35 -- 41 -- 35 -- (10)
        with 38 dropoff @36, 44 dropoff @35, 45 dropoff @40, 42 43 dropoff @41
    Cost = car 146667.33 + walk 40015 (3 + 20000 + 20000 + 12)
- Gadget3 Line : (17) -- 46 -- 47 -- 48 -- 49 -- (2)
    Should do (17) -- 46 -- (17) + (2) -- 49 -- (2) with 47 dropoff @46, 48 dropoff @49 --> cost = car 16 + walk 100000


Soda loc17 loc43 loc38 loc31 loc1 loc11 loc13 loc23 loc42 loc23 loc13 loc11 loc39 loc37 loc15 loc37 loc39 loc16 loc38 loc43 loc12 Soda


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