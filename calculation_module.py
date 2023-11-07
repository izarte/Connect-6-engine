from defines import *
from tools import is_valid_pose, my_print

import random
import sys

"""
    Class to store each direction information
"""
class CalculationData():
    def __init__(self):
        # Current color
        self.color = NOSTONE
        self.last_color = NOSTONE
        # Continuous stones
        self.continuous_n = 0
        # Total stones
        self.n = 0
        self.possible_spaces = 0
        self.spaces = 0
        self.left_spaces = 0
        self.right_spaces = 0
        self.is_last = False
    
    def reset(self):
        self.color = NOSTONE
        self.last_color = NOSTONE
        self.continuous_n = 0
        self.n = 0
        self.possible_spaces = 0
        self.spaces = 0
        self.left_spaces = 0
        self.right_spaces = 0
        self.is_last = False

"""
    Function evaluate current board configuration
    params:
        - board: 21x21 array with stone configuration
        - my_color: AI color
    returns:
        - int: difference between safety and threats
"""
def evaluate_board(board, my_color):
    # Points for AI
    safety = 0
    # Points for oponent
    threats = 0

    # Data structure for each directon searched
    h_data = CalculationData()
    v_data = CalculationData()
    d1_r_data = CalculationData()
    d1_l_data = CalculationData()
    d2_r_data = CalculationData()
    d2_l_data = CalculationData()

    for i in range(1, GRID_NUM - 1):
        # Reset all data for each line
        h_data.reset()
        v_data.reset()
        d1_r_data.reset()
        d1_l_data.reset()
        d2_r_data.reset()
        d2_l_data.reset()
        for j in range(1, GRID_NUM - 1):
            # Check if current state is last in line so, must evaluate
            h_data.is_last = j == GRID_NUM - 2
            v_data.is_last = j == GRID_NUM - 2
            # Get current position stone or empty
            h_data.color = board[i][j]
            v_data.color = board[j][i]

            # Calculate horizontal (vertical due to i,j configuration)
            safety, threats = check_actual(h_data, my_color, safety, threats)
            # Calculate vertical (horizontal due to i,j configuration)
            safety, threats = check_actual(v_data, my_color, safety, threats)

            # For diagonal searches
            if j < i:
                # Check if current state is last in line so, must evaluate
                is_last = j == i - 1
                # Store state for each line data
                d1_r_data.is_last =  is_last
                d1_l_data.is_last =  is_last
                d2_r_data.is_last =  is_last
                d2_l_data.is_last =  is_last

                # Get current position stone or empty for places below principal diagonal
                d1_r_data.color = board[j][i - j]
                d2_r_data.color = board[j][GRID_NUM - 2 - i + j]
                # If current moment doesn't belong to a principal diagonal
                if j != GRID_NUM -  2 - i + j and (i - j) != GRID_NUM - 2 - j:
                    # Get current position stone or empty for places below principal diagonal
                    d1_l_data.color = board[GRID_NUM -  2 - i + j][GRID_NUM - 2 - j]
                    d2_l_data.color = board[GRID_NUM - 2 - i + j][j]
                    # Calculate below principal diagonal for both directions
                    safety, threats = check_actual(d1_l_data, my_color, safety, threats)
                    safety, threats = check_actual(d2_l_data, my_color, safety, threats)
                # Calculate above principal diagonal for both directions
                safety, threats = check_actual(d1_r_data, my_color, safety, threats)
                safety, threats = check_actual(d2_r_data, my_color, safety, threats)

    # print(f"Safety: {safety} Threats: {threats}")
    # my_print(f"Safety: {safety} Threats: {threats}", "sco.log")
    return safety - threats


def check_actual(data, my_color, safety, threats):
    # Current position is blank
    if data.color == NOSTONE:
        # Add possible spaces count
        data.possible_spaces += 1
        # Reset contonious counter
        data.continuous_n = 0
        # Last position evaluate previous combination
        if data.is_last:
            # Last column so there is not space in "right" side
            data.right_spaces = 0
            safety, threats = evaluate(data, data.last_color, my_color, safety, threats)
        return safety, threats
    
    # my_print(f"i: {i} j: {j} data.color: {data.color}", "sco.log")
    # Same color as last seen
    if data.last_color == data.color:
        # Add counters
        data.n += 1
        data.continuous_n += 1
        # Possible spaces become true and reset
        data.spaces += data.possible_spaces
        data.possible_spaces = 0
        # If is last position
        if data.is_last:
            # Last column so there is not space in "right" side
            data.right_spaces = 0
            # Evaluate current stone counters
            safety, threats = evaluate(data, data.color, my_color, safety, threats)

    # Current color is different than last seen
    if data.color != data.last_color:
        # Anystone has been found in current line
        if data.last_color != NOSTONE:
            # Possible spaces become all right spaces for current stone configuration
            data.right_spaces = data.possible_spaces
            # Set free rigth as true as there is some counter active
            data.free_right = False
            # Evaluate current stone counters
            safety, threats = evaluate(data, data.last_color, my_color, safety, threats)
        # Possible spaces are left spaces for new configuration
        data.left_spaces = data.possible_spaces
        data.possible_spaces = 0
        # Change last color and reset counters
        data.last_color = data.color
        data.n = 1
        data.continuous_n = 1
    return safety, threats

"""
    Function to score n stones in line without oponent stones
    params:
        - n: Number of stones found in a line consecutively
    returns:
        - score: int that represents configuration score
"""
def calculate_stone_score(n):
    if n >= 4:
        return 100
    if n >= 2:
        return 50
    return 0

"""
    Function to calculate spaces score reduction 
    params:
        - n: Number of spaces found between stones
    returns:
        - score: int that represents score reduction
"""
def calculate_spaces_score(n):
    if n <= 2:
        return 1
    return (n // 2 + n % 2)

"""
    Function to caclculate score for current stone configuration:
    params:
        - data: (CalculationData) data with stone line information
        - color: current stone color
        - my_color: AI color
        - safety: score for AI
        - threats: score for oponent
    returns:
        - safety: modified if color == my_color
        - threats: modified if color != my_color
"""
def evaluate(data, color, my_color, safety, threats):
    free_left = data.n + data.left_spaces >= 6
    free_right = data.n + data.right_spaces >= 6
    value = calculate_stone_score(data.n) / calculate_spaces_score(data.spaces)
    score = value * (1 + free_left + free_right)
    if data.n >= 6 and data.spaces == 0:
        score = MAXINT
    # if score != 0:
    #     print(f"n: {data.n} spaces: {data.spaces} left: {data.left_spaces} right: {data.right_spaces}")
    if not free_left and not free_right and data.n + data.spaces < 6:
            score = 0
    if color == my_color:
        safety += score
    else:
        threats += score
    return safety, threats

                    
class CalculationModule():
    def calculate():
       return random.randint(-sys.maxsize, sys.maxsize)