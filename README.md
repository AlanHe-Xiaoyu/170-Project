# project-fa19
CS 170 Fall 2019 Project
# 170-Project

## Sources:
1. TSP solver : Google optimization team https://developers.google.com/optimization/routing/vrp
2. Simulated annealing : https://github.com/perrygeo/simanneal
3. We implemented K-clustering following from the pseudocode on the textbook

## How to run?
1. python3 solver.py --all inputs final_outputs
- If anything fails, drag it out, and rerun individually at the very end
2. python3 compress_output.py final_outputs/




## Rest are for our own purposes

11_50 : 10.219
11_100 : 52.718
11_200 : 13.284

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

# FINAL REPORT

441 words right now

The report should be a summary of how your algorithm works, what other methods you tried along the way, and what computing resources you used (e.g. AWS, instructional machines, etc.). Your final report should be at least 400 words, and no more than 1000 words long. You will also submit the code for your solver, along with a README containing precise instructions on how to run it. 


Essentially, we implemented the strategies outlined in the initial reports, including a naive baseline that simply drops all students off at “Soda” - starting car location - which works surprisingly well on some inputs as we visualized some of them selectively. Then, we decided to go a little deeper, which involves a more advanced baseline that solves a TSP based on all homes. This is done by viewing only a subgraph of the original graph consisting of only the homes and starting location, and then use the all pairs Dijkstra’s result to fake an edge between any pair of homes even if there isn’t one. We then continue working on this path by randomly selecting a subset of homes to run our fakeTSP on. The random selection is done simply through random.random and setting a seed initially. The TSP solver we use is developed by Google.

Note: due to the large portion of grades allotted to solving our own inputs, we put extra hyper parameters and tried different seeds to find the best outputs we can find on our own inputs, and then insert a special check to return our own “optimal” solution directly if the input matches with our input’s pattern.

Afterwards, we implemented k-clustering for homes and then picking the center of each cluster to run this fakeTSP. The code follows from the idea in textbook, and after running it for a while, we discovered that this is more or less similar to randomly selecting a subset of all homes and fine-tuning the selectivity.

Being stuck on a local minimum, we decided to use some method to further improve our results. The one thing we found was simulated annealing. It was difficult to define the transition probabilities, so we decided to just randomly select pairs and see if it improves anything. This doesn’t help too much, so we implemented general TSP from an online paper. We always compare results with previous ones and change them only if we’ve got an improvement.

We used Google Cloud Platform for about an hour or so, and discovered that it didn’t help with our efficiency too much. The main problem was that our Python kept giving a segmentation fault, so we wrote a script to basically continue from where it left off from the original inputs. Then, we could finish the inputs rather quickly. Lastly, we visualize inputs that always gives us a segfault, visualize it online, and basically do a special manual solve on each of them - there’s about 10-20 of them, mostly consisting of fully-connected graphs or star-like graphs, and both of which are very easy to figure out the optimum. These are also specially detected/conditioned to directly return the optimum we’ve found. In cases where it’s just fully-connected or star-like graphs, we basically ran the optimum solver for these two specific types of graphs on all inputs and compare with previous solutions to see which one’s better.