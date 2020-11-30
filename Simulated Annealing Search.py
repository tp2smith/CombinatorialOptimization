# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 19:22:52 2020

@author: Taylor
"""

import random
import math
import matplotlib.pyplot as plt
import time

grid1 = [[3,7,2,8],[5,2,9,1],[5,3,3,1]]
#largest value is 9

grid2 = [[0,0,0,1,4],[0,0,2,8,10],[0,0,2,4,12],[0,2,4,8,16],[1,4,8,16,32]]
#largest value is 32

f = lambda x,y: -(1-x)**2  - 100*(y - x**2)**2

a,b,c,d,=-2,2,-1,3

grid3 = [[f(a + i*(b-a)/99, c + j*(d-c)/99) for j in range(100)] for i in range(100)] 
#plt.plot([[grid3[j][i] for i in range(100)] for j in range(100)],[i for i in range(100)])
#largest value is -0.00010307142541639527

"""
This class is created to store information about the current node being examined.

indexRow = The row index the current value is assigned too.
indexCol = The column index the current value is assigned too.
value = The value of the current node.

It is created in the following way: Node(indexRow, indexCol, value)

Ex - [[1,2,3],[2,4,5],[4,8,1]]. 
The value of 8 would be represented in the following way:
    Node(2,1,8).
"""
class Node:
    def __init__ (self, indexRow, indexCol, value):
        self.indexRow = indexRow
        self.indexCol = indexCol
        self.value = value

"""
This function creates the nodes based on the 4 possible actions that can be taken in the matrix.
1. Up
2. Down
3. Right
4. Left
"""
def make_nodes(node,grid,row,col):
    new_nodes = list()
    #check actions to make on grid
    if node.indexRow + 1 <= row:
        down_node = Node(node.indexRow + 1,node.indexCol, grid[node.indexRow + 1][node.indexCol])
        new_nodes.append(down_node)
    if node.indexRow - 1 >= 0:
        up_node = Node(node.indexRow - 1,node.indexCol, grid[node.indexRow - 1][node.indexCol])
        new_nodes.append(up_node)
    if node.indexCol - 1 >= 0:
        left_node = Node(node.indexRow, node.indexCol - 1, grid[node.indexRow][node.indexCol - 1])
        new_nodes.append(left_node)
    if node.indexCol + 1 <= col:
        right_node = Node(node.indexRow, node.indexCol + 1, grid[node.indexRow][node.indexCol + 1])
        new_nodes.append(right_node)
    return new_nodes
    
"""
This is the main function, where the searching takes place.

This operates by setting a search threshold of 250000000 (largest value that made sense).
Then, setting the bounds for the Temperatures, a lower and upper bound in order to
ensure earlier searchs have a higher probability of going the 'wrong' direction.

One the search begins, it will find possible new nodes, assess them based on the following process:
    1. Is it higher then the current node? If yes, then make it the current node.
    2. If it is not higher then the current node, a probability is calculated based on the 
    change in energy between the new node and the current node and the current temperature
    and if it is higher then a random value between 0 and 1 (higher probabilities will have a 
    better chance of being chosen).
    
This will keep looping through until the Temperature has "cooled" sufficiently.
"""

def simmulated_annealing (grid):
    start_time = time.time()
    n = 250000000
    #pMax = 0.7
    #pMin = 0.001
    #tMax = -1/math.log(pMax)
    #tMin = -1/math.log(pMin)
    tMax = 1
    tMin = 0.01
    #frac = (tMax/tMin)**(1.0/(n-1.0))
    max_rows = len(grid) - 1
    max_columns = len(grid[0]) - 1
    prev_node = 0
    current_node = Node(0, 0, grid[0][0])
    t = tMax
    step = 0
    p_list = []
    p_count_list = []
    delta_list = []
    p_count = 0
    node_list = []
    step_list = []
    # print (i,j,initial_state)
    while tMin <= t:
        next_node = make_nodes(current_node, grid, max_rows, max_columns)
        for elem in next_node:
            if elem.value > current_node.value:
                current_node = elem
                node_list.append(current_node.value)
                step_list.append(step)
                step += 1
                t = t - (step/n)
            else:
                prev_node = current_node
                current_node = elem
                delta = abs(current_node.value - prev_node.value)
                delta_list.append(delta)
                p = math.exp(-delta/t)
                p_list.append(p)
                p_count_list.append(p_count)
                p_count += 1
                if random.random() > p:
                    current_node = prev_node
                    node_list.append(current_node.value)
                    step_list.append(step)
                    step += 1
                    t = t - (step/n)
                else:
                    node_list.append(current_node.value)
                    step_list.append(step)
                    step += 1
                    t = t - (step/n)
        #print(current_node.value)
    #plt.plot([p_count_list[i] for i in range(p_count)],[p_list[i] for i in range(p_count)])
    #plt.plot([p_count_list[i] for i in range(p_count-200, p_count)],[delta_list[i] for i in range(p_count-200,p_count)])
    #plt.plot([step_list[i] for i in range(step-500,step)],[node_list[i] for i in range(step-500,step)])
    end_time = time.time()
    total_time = end_time - start_time
    print("The total time spent finding the maximum solution was: ",total_time)
    return current_node

"""
This initializes the grids, along with running the simulated annealing algorithm.
"""
def main():
    # Initialize the Grids
    grid1 = [[3,7,2,8],[5,2,9,1],[5,3,3,1]]
    grid2 = [[0,0,0,1,4],[0,0,2,8,10],[0,0,2,4,12],[0,2,4,8,16],[1,4,8,16,32]]
    f = lambda x,y: -(1-x)**2  - 100*(y - x**2)**2
    a,b,c,d,=-2,2,-1,3
    grid3 = [[f(a + i*(b-a)/99, c + j*(d-c)/99) for j in range(100)] for i in range(100)] 
    max_value1 = simmulated_annealing(grid1)
    print ("The maximum value found in grid1 was: ",max_value1.value)
    max_value2 = simmulated_annealing(grid2)
    print ("The maximum value found in grid2 was: ",max_value2.value)
    max_value3 = simmulated_annealing(grid3)
    print ("The maximum value found in grid3 was: ",max_value3.value)

main()