# CombinatorialOptimization
Repository of my Math 3172 Class Assignments, Midterms, and Final Exams. Shows examples of AStar Search, Monte Carlo Tree Search, and the Traveling Salesman Problem.

See descriptions of the different problems that were solved:


## AStar Search - Pancake Problem
Pancake sorting is the colloquial term for the mathematical problem of sorting a disordered stack of pancakes in order of size when a spatula can be inserted at any point 
in the stack and used to flip all pancakes above it. A pancake number is the minimum number of flips required for a given number of pancakes.

The AStar Seach Algorithm traverses through a tree by keeping in mind the current cost spent to traverse from the starting node to the current node and the estimated
movement cost of chosing a specific node in its relation to the destination. This is described as a heuristic function.


## Monte Carlo Tree Search - Adversarial Search
The Adversarial Search problem being solved is a game of tic tac toe. The AI will learn over time how to play against you, as the second player.

The Monte Carlo Tree Search algorithm focuses on a method that is usually used in games to predict the path (moves) that should be taken by the policy 
to reach the final winning solution. It does this by:
* 1 Selecting a node from the tree that has the best chance to win.
* 2 Expanding and creating the many children nodes that result from choosing the previous node.
* 3 Simulating/Exploring along the possible path options in order to determine where the best path lies.
* 4 Back-Propogate the newly discovered information into the paths, in order to make a better path decision in the future.


## Two Opt Search - Traveling Saleman Problem 
The Traveling Salesman problem is a classic optimization problem, where you answer the following question: asks the following question: 
"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"

This runs the Two Opt Search algorithm, which will compare every possible valid combination of the swapping mechanism, which will systematically change routes along each city
to determine the most effective route.

This code addionally scraps data directly from a University of Waterloo website in order to solve the problem.
