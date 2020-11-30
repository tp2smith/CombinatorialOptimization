# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:46:21 2020

@author: Taylor
"""

import re
import math
import random
import matplotlib.pyplot as plt
import time
import requests
from bs4 import BeautifulSoup
import copy
from functools import lru_cache
import collections
import numpy as np

"""
This class is created to store information about the current node being examined.

cityIndex = The index the current city.
parentCityIndex = The city that was previously visited.
xCoord = The x coordinate of the city that was given.
yCoord = The y coordinate of the city that was given.
f = The current total distance of the trip.
g = The distance between this city and the parent city.

It is created in the following way: Map(cityIndex, parentCityIndex, xCoord, yCoord, f, g)
"""
class City_Node:
    def __init__(self, cityIndex, xCoord, yCoord, f):
        self.cityIndex = cityIndex
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.f = f

"""
This function caluclates the euclidean distance between two cities.
"""
#@lru_cache(maxsize=None)
def distance_function (x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#@lru_cache(maxsize=None)
def edge_check (a,b,c,d,e):
    new_distance = distance_function(a.xCoord,a.yCoord,c.xCoord,c.yCoord) + distance_function(b.xCoord,b.yCoord,d.xCoord,d.yCoord)
    current_distance = distance_function(b.xCoord,b.yCoord,c.xCoord,c.yCoord) + distance_function(e.xCoord,e.yCoord,d.xCoord,d.yCoord)
    return new_distance - current_distance
"""
This function finds a states index based on a list of remaining states, removing
that state in the process. This is used to bring the next city up in the trip.
"""
def state_search(state_list, index):
    i = 0
    for elem in state_list:
        if elem[0] == index:
            state = elem
            del state_list[i]
            break
        i += 1
    return state,state_list
"""
Initialize the file to use in algorithm coordinates follow the format 
[cityIndex, x-coord, y-coord] import txt file and create list of coordinates 
of cities for use.
"""
def initialize(text_file):
    #coord_text_file = open(text_file, 'r')
    #coord_content = coord_text_file.read()
    coord_content = text_file
    djiboutiCityCoords = list()
    coord_content = re.sub("\n", "|",coord_content)
    coord_content = re.sub("\s", ",",coord_content)
    coord_content_final = coord_content.split('|')
    for elem in coord_content_final: 
        elem = elem.split(',')
        djiboutiCityCoords.append(elem[0:3])
    del djiboutiCityCoords[0:7]
    del djiboutiCityCoords[len(djiboutiCityCoords)-2:len(djiboutiCityCoords)]
    index = random.randint(0,len(djiboutiCityCoords)-1)
    initial_city = list(djiboutiCityCoords[index])
    del djiboutiCityCoords[index]
    return initial_city, djiboutiCityCoords

"""
This is the initial path creation based on minimum distance and a random start point.

It is based off the randomized_nearest_neighbours algorithm.

First the initial city is created, and then the remaining cities are cycled through
based on the next closest city to create an initial trip.

This will then be used for further optimizations.
"""
def randomized_nearest_neighbours(initial_state, remaining_states):
    current_state = initial_state
    history_states = list()
    min_distance = tuple()
    new_state = tuple()
    while remaining_states != []:
        distance_dict = list()
        for elem in remaining_states:
            hp.heappush(distance_dict,(distance_function(float(elem[1]),float(elem[2]),current_state.xCoord, current_state.yCoord),elem[0]))
        min_distance, state = hp.heappop(distance_dict)
        new_state = state_search(remaining_states, state)
        remaining_states = new_state[1]
        history_states.append(current_state)
        current_state = City_Node(new_state[0][0], float(new_state[0][1]), float(new_state[0][2]), current_state.f + min_distance)
        min_distance = 0
        new_state = tuple()
    history_states.append(current_state)
    final_distance_segment = distance_function(initial_state.xCoord, initial_state.yCoord,current_state.xCoord, current_state.yCoord)
    final_state = City_Node(initial_state.cityIndex, initial_state.xCoord, initial_state.yCoord, current_state.f + final_distance_segment)
    history_states.append(final_state)
    return history_states
"""
This is the algorithm that will optimize the first found solution using the
2-opt approach, or switching the path between two cities until an optimized
solution is found.

The first and last element before switching are kept in case the new path
is not optimal.

def edge_check (a,b,c,d,e):
    new_distance = distance_function(a.xCoord,a.yCoord,c.xCoord,c.yCoord) + distance_function(b.xCoord,b.yCoord,d.xCoord,d.yCoord)
    current_distance = distance_function(b.xCoord,b.yCoord,c.xCoord,c.yCoord) + distance_function(e.xCoord,e.yCoord,d.xCoord,d.yCoord)
    return new_distance - current_distance

This will run for 10 full complete iterations.
"""
def two_opt_algorithm(rnn_solution):
    current_path = copy.deepcopy(rnn_solution)
    attempts = 0
    total_time = 0
    diff = 0
    new_path = list(current_path)
    while (attempts < 500):
        start_time = time.time()
        for i in range(0, len(current_path)-2):
            for j in range(i+2, len(current_path)):
                if i == 0 and j == len(current_path) - 1:
                    diff = 0
                elif i == 0:
                    diff = edge_check(current_path[0],current_path[j],current_path[j+1],current_path[-2],current_path[-1])
                elif j == len(current_path) - 1:
                    diff = edge_check(current_path[j],current_path[i],current_path[i-1],current_path[1],current_path[0])
                else:
                    diff = edge_check(current_path[i],current_path[j],current_path[j+1],current_path[i-1],current_path[i])
                if (diff < 0):
                    if i == 0:
                        new_path = new_path[j::-1] + new_path[j+1:len(current_path)-1] + [new_path[j]]
                    elif j == len(current_path) - 1:
                        new_path = [new_path[i]] + new_path[1:i] + new_path[j:i-1:-1]
                    else:
                        new_path = new_path[:i] +  new_path[j:i-1:-1] +  new_path[j+1:len(current_path)]
                    current_path = tuple(new_path)
        attempts += 1
    end_time = time.time()
    time_diff = end_time - start_time
    total_time = total_time + time_diff
    new_built_path = build_city_path(current_path)
    return new_built_path

"""
Make updates to ensure that you only calculate the diff between the two point switches. 
This will improve your calc time, and should make for a faster processing.

Add in the pyplot an actual map of the coutnry you are doing, see if you can 
transform the data so it perfectly lies on a map of Finland.
"""

"""
This function will recalculate the new trip distance based on the 2-Opt path
change that was made.
"""                   
def build_city_path(path):
    updated_path = list()
    for i in range(0,len(path)-1):
        updated_distance = distance_function(path[i].xCoord,path[i].yCoord,path[i+1].xCoord,path[i+1].yCoord)
        if (i == 0):
            f_value = 0
            first_node = City_Node(path[i].cityIndex,path[i].xCoord,path[i].yCoord, f_value)
            updated_path.append(first_node)
            f_value = updated_distance
            new_node = City_Node(path[i+1].cityIndex,path[i+1].xCoord,path[i+1].yCoord, f_value)
            updated_path.append(new_node)
        else:
            f_value += updated_distance
            new_node = City_Node(path[i+1].cityIndex,path[i+1].xCoord,path[i+1].yCoord, f_value)
            updated_path.append(new_node)
    return updated_path        

"""
This uploads the data, transforms it, finds an initial path, and then optimizes it after
finilzing everything by plotting the points.
"""

def main():
    URL = 'http://www.math.uwaterloo.ca/tsp/world/qa194.tsp'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    map_coord_file = soup.text
    initial_prompt = initialize(map_coord_file)
    start_time = time.time()
    initial_state = City_Node(initial_prompt[0][0], float(initial_prompt[0][1]), float(initial_prompt[0][2]),0)
    solution = randomized_nearest_neighbours(initial_state,initial_prompt[1])
    #i = 1
    print("The first solution found is as stated: \n")
    """for elem in solution:
        print("City number ",elem.cityIndex, " is visited as the number",i, "city, having traveled a distance of ",elem.f,"kms thus far. \n")
        i += 1"""
    print("City number ",solution[-1].cityIndex, " is visited as the number 4664 city, having traveled a distance of ",solution[-1].f,"kms thus far. \n")
    optimized_solution = two_opt_algorithm(solution)
    print("The optimized solution found is as stated: \n")
    #i = 1
    """for elem in optimized_solution:
        print("City number ",elem.cityIndex, " is visited as the number",i, "city, having traveled a distance of ",elem.f,"kms thus far. \n")
        i += 1"""
    print("City number ",optimized_solution[-1].cityIndex, " is visited as the number 4664 city, having traveled a distance of ",optimized_solution[-1].f,"kms thus far\n")
    n = len(optimized_solution)
    solutionCoords = [[elem.xCoord,elem.yCoord] for elem in optimized_solution]
    plt.plot([solutionCoords[i][0] for i in range(n)],[solutionCoords[i][1] for i in range(n)],'xk-')
    plt.title('Qatar TSP Optimized Solution')
    plt.xlabel('X-Coordinate')
    plt.ylabel('Y-Coordinate')
    fig = plt.gcf()
    fig.set_size_inches(10.5, 10.5, forward=True)
    plt.ion()
    plt.show()
    end_time = time.time()
    total_time = end_time - start_time
    print("The total time spent finding the best solution was: ",total_time)
    return optimized_solution,
answer = main()



