# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:34:15 2020

@author: Taylor
"""
import time
import random
import numpy as np
from copy import deepcopy
from collections import defaultdict

"""
This code was created with assistance from the following source.
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1 
"""

"""
This set of actions defines an action dictionary of possible moves.
"""
action_values = dict()
action_values["Top Left"] = [0,0]
action_values["Top Centre"] = [0,1]
action_values["Top Right"] = [0,2]
action_values["Middle Left"] = [1,0]
action_values["Middle Centre"] = [1,1]
action_values["Middle Right"] = [1,2]
action_values["Bottom Left"] = [2,0]
action_values["Bottom Centre"] = [2,1]
action_values["Bottom Right"] = [2,2]

class MCTN:
    "This class defines a Monte Carlo Tree that can be used in a Monte Carlo Tree Searcher"
    
    
    """
    parent - The parent node of the tic tac toe board.
    state - The current board layout.
    R - current rewards that have been found following this node.
    V - current number of visits to this node and all children of this node.
    children - List of nodes that are the children to current node.
    playerOne - True to indicate if 'x', and False to indicate if 'o'.
    actionsLeft - Number of unexplored actions reminings for node.
    """
    def __init__(self, state, playerOne, parent = None, actionsLeft = 9):
        self.parent = parent
        self.state = state
        self.R = 0
        self.V = 0
        self.children = []
        self.playerOne = playerOne
        self.actionsLeft = actionsLeft

    """
    This will rollout the current board that was played and is simulated.
    Additionally includes the select, expand, and backpropogation aspects
    of the Monte Carlo Tree Search.
    """
    def rollout(self):
        root_node = self
        current_state = self
        terminalState = False
        while terminalState == False:
            test_eval = current_state.evaluation()
            if not type(test_eval) == str:
                break
            if current_state.actionsLeft != 0 :
                current_state = current_state.expand()
            else:
                current_state = current_state.select()
        reward = current_state.evaluation()
        current_state.backprop(reward)
        return root_node.select(c_param = 0.5) # this value heavily favours visits and rewards.
    

    
    """
    Evaluates the current board to determine what score will be assigned to it
    as well as if the board is complete.
    """    
    def evaluation(self):  
        if ((self.state[0][0] == 'x' and self.state[0][1] == 'x' and self.state[0][2] == 'x')
        or (self.state[1][0] == 'x' and self.state[1][1] == 'x' and self.state[1][2] == 'x')
        or (self.state[2][0] == 'x' and self.state[2][1] == 'x' and self.state[2][2] == 'x')):
            return 1
        elif ((self.state[0][0] == 'o' and self.state[0][1] == 'o' and self.state[0][2] == 'o')
        or (self.state[1][0] == 'o' and self.state[1][1] == 'o' and self.state[1][2] == 'o')
        or (self.state[2][0] == 'o' and self.state[2][1] == 'o' and self.state[2][2] == 'o')):
            return 0
        elif ((self.state[0][0] == 'x' and self.state[1][0] == 'x' and self.state[2][0] == 'x')
        or (self.state[0][1] == 'x' and self.state[1][1] == 'x' and self.state[2][1] == 'x')
        or (self.state[0][2] == 'x' and self.state[1][2] == 'x' and self.state[2][2] == 'x')):
            return 1
        elif ((self.state[0][0] == 'o' and self.state[1][0] == 'o' and self.state[2][0] == 'o')
        or (self.state[0][1] == 'o' and self.state[1][1] == 'o' and self.state[2][1] == 'o')
        or (self.state[0][2] == 'o' and self.state[1][2] == 'o' and self.state[2][2] == 'o')):
            return 0
        elif ((self.state[0][0] == 'x' and self.state[1][1] == 'x' and self.state[2][2] == 'x')
        or (self.state[2][0] == 'x' and self.state[1][1] == 'x' and self.state[0][2] == 'x')):
            return 1
        elif ((self.state[0][0] == 'o' and self.state[1][1] == 'o' and self.state[2][2] == 'o')
        or (self.state[2][0] == 'o' and self.state[1][1] == 'o' and self.state[0][2] == 'o')):
            return 0
        elif sum([self.state[i].count('_') for i in range(3)]) == 0 :
            return 0.5
        else: 
            return "Not Terminal"

    """
    If node is fully unexplored, then it will randomly select the next potential node to play.
    """
    def next_random_action(self):
        global action_values
        children_list = []
        for c in self.children:
            children_list.append(c.state)
        action_num = 0
        new_state = deepcopy(self.state)
        if self.playerOne == True:
            symbol = 'x'
        else:
            symbol = 'o'
        correctMove = False
        while correctMove == False:
            board_row, board_col = random.randint(0,2), random.randint(0,2)
            if new_state[board_row][board_col] == "_" and not (new_state in children_list):
                new_state[board_row][board_col] = symbol
                correctMove = True
                action_num = 1
        return new_state, action_num
            
    """
    Defines the selection process based on the UCB formula (upper confidence bound)
    """
    def select(self, c_param = 1.4):
        test_list = []
        for c in self.children:
            test_list.append(c)
        choice_uct_list = [
                c.R / c.V + c_param * np.sqrt((2*np.log(self.V) / c.V))
                for c in self.children
                ]
        return self.children[np.argmin(choice_uct_list)] #only for playing against circle, max when playing against cross
    
    """
    Defines the expansion process when a node is not fully expanded.
    """
    def expand(self):
        next_state, actions = self.next_random_action()
        child_node = MCTN(next_state,parent=self, playerOne = not self.playerOne, actionsLeft=sum([next_state[i].count('_') for i in range(3)]))
        self.children.append(child_node)
        self.actionsLeft -= actions
        return child_node
    
    """
    Defines the backprop process once a terminal state has been reached. This
    runs back up the tree until a value is reached.
    """
    def backprop(self, reward):
        self.R += reward
        self.V += 1
        if self.parent:
            self.parent.backprop(reward)
    
    """
    Defines a process to go back up the tree to the root node to restart the game.
    """
    def root_cycle(self):
        root_node = self
        if self.parent:
            root_node = self.parent.root_cycle()
        return root_node
    
"""
This runs the main parts of the code, and generates the boards as you play.
There are 50 full games that can be played.
"""
def main():
    games_played = 50
    starting_board = MCTN([['_','_','_'],['_','_','_'],['_','_','_']],True,None)
    action_keys = list(action_values.keys())
    while games_played != 0:
        print("To play the game, enter in any of the following commands\n")
        for item in action_keys:
            print(item,"\n")
        if games_played != 50:
            starting_board = starting_board.root_cycle()
        while True:
            new_board = deepcopy(starting_board)
            correctMove = False
            while correctMove == False:
                playerInput = input("Player 1 enter your move: ")
                if playerInput in action_keys:
                    move = action_values[playerInput]
                else:
                    print("Input was incorrect. Try again!")
                if starting_board.state[move[0]][move[1]] == "_":
                    correctMove=True
                else:
                    print("Space is already take! Choose another.")
            temp_board = deepcopy(starting_board.state)
            temp_board[move[0]][move[1]] = "x"
            children_list = []
            for c in starting_board.children:
                children_list.append(c.state)
            if not (temp_board in children_list): 
                new_board = MCTN(temp_board, playerOne = not starting_board.playerOne, parent = starting_board, actionsLeft = sum([temp_board[i].count('_') for i in range(3)]))
                starting_board.children.append(new_board)
                starting_board.actionsLeft -= 1
                starting_board = new_board
            else:
                for c in starting_board.children:
                    if c.state == temp_board:
                        starting_board = c
            for line in starting_board.state:
                print(line,"\n")
            test_eval = starting_board.evaluation()
            if test_eval == 0:
                print("Player 2 has won!")
                starting_board.backprop(test_eval)
                break
            if test_eval == 1:
                print("Player 1 has won!")
                starting_board.backprop(test_eval)
                break
            elif test_eval == 0.5:
                print("It is a tie!")
                starting_board.backprop(test_eval)
                break
            else:
                pass
            start_time = time.time()
            for _ in range(1000):
                next_move = starting_board.rollout()
            end_time = time.time()
            print("This decision took this many seconds to decide",end_time - start_time)
            starting_board = next_move
            print("Player Two's move is: \n")
            for line in starting_board.state:
                print(line,"\n")
            test_eval = starting_board.evaluation()
            if test_eval == 0:
                print("Player 2 has won!")
                starting_board.backprop(test_eval)
                break
            if test_eval == 1:
                print("Player 1 has won!")
                starting_board.backprop(test_eval)
                break
            elif test_eval == 0.5:
                print("It is a tie!")
                starting_board.backprop(test_eval)
                break
            else:
                pass
        games_played -= 1
main()        