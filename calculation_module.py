from defines import *
from tools import is_valid_pose

import random
import sys

def evaluate_board(board, my_color):
    score = [0, 0]
    for i in range(1, GRID_NUM - 1):
        for j in range(1, GRID_NUM - 1):
            if board[i][j] == NOSTONE:
                continue
            color = board[i][j]
            s = evaualte_stone(board, color, i, j)
            increment = -1
            if my_color == color:
                increment = 1
            score[0] = score[0] + increment * s[0]
            score[1] = score[1] + increment * s[1]
    
    return score


def evaualte_stone(board, color, i, j):
    axis = ['x', 'y', 'xy']
    directions = {'x': (0, 1), 'y': (1, 0), 'xy': (1, 1)}
    results = {'x': {'tiles': 0, 'blanks': 0}, 'y': {'tiles': 0, 'blanks': 0}, 'xy': {'tiles': 0, 'blanks': 0}}
    result = [0, 0]
    for ax in axis:
        look_negative = True
        look_positive = True
        possible_blanks = 0
        # Look 5 adjacent tiles
        for k in range(1,6):
            for d in [-1 * look_negative, 1 * look_positive]:
                # Stop looking if its outside board or oponent color stone has been found
                if d == 0:
                    continue
                # Current pose
                c_i = i + d * k * directions[ax][0]
                c_j = j + d * k * directions[ax][1]
                if is_valid_pose(c_i, c_j):
                    if board[c_i][c_j] == color:
                        results[ax]['tiles'] += 1
                        results[ax]['blanks'] += possible_blanks
                        possible_blanks = 0
                    if board[c_i][c_j] == NOSTONE:
                        possible_blanks += 1
                    if possible_blanks == 3 or board[c_i][c_j] == color ^ 3:
                        if d == 1:
                            look_positive = False
                        if d == -1:
                            look_negative = False
        result[0] += results[ax]['tiles']
        result[1] += results[ax]['blanks']
        
        return result

                    
class CalculationModule():
    def calculate():
       return random.randint(-sys.maxsize, sys.maxsize)