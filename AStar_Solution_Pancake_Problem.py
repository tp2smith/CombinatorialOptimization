# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:46:58 2020

@author: Taylor
"""

import random
import heapq as hp
from decimal import *

def h_function(s):
    """
    The heuristic function calculates the forward cost based on comparing the 
    current order of the pancakes and the maximum distance between each pancake
    and the expected placement. 
    I.e for 5 pancakes, if the pancakes were [0,2,4,1,3], then the h would be
    2 because the max distance between a pancake and its end state is 2 movements.
    """
    h_value = max([abs(s[i]-i) for i in range(len(s)-1)])
    return h_value

def a_star_pancake_problem ():
    
    """
    Ask the user to submit a number indicating how large they wish the pancake stack to be.
    From this, it creates the initial pancake stack.
    The pancakes range from smallest to largest, and size is associated to the
    number in the list.
    Ex - 0 is the smallest pancake in a stack of 5, and 4 would be the largest.
    """
    print("Please insert a number to indicate the number of pancakes to be sorted/flipped:")
    n = int(input())
    initial = tuple(range(0,n))
    goal_state = tuple(range(0,n))
    
    """
    Reorders the pancake stack in a random way for solving.
    """
    initial = tuple(random.sample(initial, len(initial)))
    
    """
    Calculates the initial states future cost
    """
    h = h_function(initial)
    
    """
    initialize the three dictionaries used. 
    queue: a dictionary of the nodes to visit next
    nodes_explored: a set of node states previously visited to prevent 
    visited states from being explored.
    current_node_inspect: a dictionary of the current node being visited
    """
    nodes_explored = set()
    
    """
    Nodes have 4 elements:
    f (g+h): cost of steps through problem plus future cost.
    State: current state
    Parent: parent state
    g: cost of steps through problem
    """
    queue = [(0+h,initial,None,0)]
    
    goal_state_answer = False
    
    """
    The while loop will check if current node is the goal state, if not
    then it will explore further nodes and add the new
    current_node to be inspected from the front of the queue.
    """
    while(goal_state_answer == False):
        # creates a list of node states already visited for quick reference
        # initial state node placed into nodes_explored dictionary
        
        current_node = hp.heappop(queue)
        
        if current_node[1] == goal_state:
            goal_state_answer = True
            break
        
        nodes_explored.add(current_node[1])
        
        # temp output list of explored nodes to be placed into queue
        
        current_node, queue = create_nodes(current_node, nodes_explored, queue)
        
    print ("Solution found")
    print ("The initial state was: %s" % str(initial))
    print ("The final state was: %s" % str(current_node[1]))
    print ("This was completed in %s flips" % str(current_node[0]))

""" 
create_nodes: creates the new potential nodes based on there being n different ways
to flip the stack of pancakes. Will not explore nodes if already visited.
"""
def create_nodes(node, explored, queue):
    
    f, current_node, current_parent_index, current_path_cost = node
    
    n = len(node[1])
    
    for i in range(1,n+1):
        temp = list(current_node)
        flip_list = list(temp[0:i])
        flip_list.reverse()
        for j in range(0,i):
            temp[j] = flip_list[j]
        new_node = tuple(temp)
        if not(new_node in explored): 
           h_value = h_function(new_node)
           hp.heappush(queue, (current_path_cost+1+h_value,new_node,current_parent_index,current_path_cost+1))
     
    return node, queue

# Activate the algorithm to solve for the Goal State.
a_star_pancake_problem()