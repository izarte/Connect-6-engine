from defines import *
# from tools import is_valid_pose, my_print

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


class BoardScore():
    def __init__(self):
        self.safety = 0
        self.possible_safety = 0
        self.threats = 0
        self.possible_threats = 0
        self.weights = []
        self.win = 0
        self.lose = 0
        self.same = 0
        self.opponent = 0
        self.my_frees = 0
        self.opponent_frees = 0
    
    def set_weights(self, weights):
        self.weights = weights
        # self.weights = [50, 15, -100, -10]
    
    def ponderate(self, t):
        if self.win > 0:
            return MAXINT
        if self.lose > 0 or self.threats:
            return MININT
        score = self.weights[0] * self.safety
        if t:
            print(self.weights[0], ":", score, end=' ')
        score += self.weights[1] * self.possible_safety
        if t:
            print(self.weights[1], ":", score, end=' ')
        score += self.weights[2] * self.threats
        if t:
            print(self.weights[2], ":", score, end=' ')
        score += self.weights[3] * self.possible_threats
        if t:
            print(self.weights[3], ":", score, end=' ')
            print()
        score += self.weights[4] * self.same
        score += self.weights[5] * self.opponent
        score += self.weights[6] * self.my_frees
        score += self.weights[7] * self.opponent_frees
        return score

    def __str__(self):
        return f"Safety: {self.safety} possible_safety: {self.possible_safety} threats: {self.threats} possible_threats: {self.possible_threats}"


"""
    Function evaluate current board configuration
    params:
        - board: 21x21 array with stone configuration
        - my_color: AI color
    returns:
        - int: difference between safety and threats
"""
def evaluate_board(board, my_color, moves, genetic_weights = None, t=False):
    # Evaluation metrics
    board_score = BoardScore()

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
            board_score = check_actual(h_data, my_color, board_score)
            # Calculate vertical (horizontal due to i,j configuration)
            board_score = check_actual(v_data, my_color, board_score)

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
                    board_score = check_actual(d1_l_data, my_color, board_score)
                    board_score = check_actual(d2_l_data, my_color, board_score)
                # Calculate above principal diagonal for both directions
                board_score = check_actual(d1_r_data, my_color, board_score)
                board_score = check_actual(d2_r_data, my_color, board_score)

    for move in moves.positions:
        window = board[move.x - 1: move.x + 2, move.y - 1: move.y + 2]
        same_color = (WHITE == my_color)
        board_score.same += np.count_nonzero(window == (same_color + 1))
        board_score.opponent += np.count_nonzero(window == ((not same_color) + 1))

    # print(board_score)
    if genetic_weights:
        if t:
            print("DATA: ", board_score.safety, board_score.possible_safety, board_score.threats, board_score.possible_threats, board_score.win, board_score.lose)
        board_score.set_weights(genetic_weights)
        score = board_score.ponderate(t)
    else:
        score = board_score.safety - board_score.threats

    # print(f"Safety: {safety} Threats: {threats}")
    # my_print(f"Safety: {safety} Threats: {threats}", "sco.log")
    return score


def check_actual(data, my_color, board_score):
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
            board_score = genetic_evaluation(data, data.last_color, my_color, board_score)
        return board_score
    
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
            board_score = genetic_evaluation(data, data.color, my_color, board_score)

    # Current color is different than last seen
    if data.color != data.last_color:
        # Anystone has been found in current line
        if data.last_color != NOSTONE:
            # Possible spaces become all right spaces for current stone configuration
            data.right_spaces = data.possible_spaces
            # Set free rigth as true as there is some counter active
            data.free_right = False
            # Evaluate current stone counters
            board_score = genetic_evaluation(data, data.last_color, my_color, board_score)
        # Possible spaces are left spaces for new configuration
        data.left_spaces = data.possible_spaces
        data.possible_spaces = 0
        # Change last color and reset counters
        data.last_color = data.color
        data.n = 1
        data.continuous_n = 1
    return board_score

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
def evaluate(data, color, my_color, board_score):
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
        board_score.safety += score
    else:
        board_score.threats += score
    return board_score

                    
def genetic_evaluation(data, color, my_color, board_score):
    free_left = data.n + data.left_spaces >= 6
    free_right = data.n + data.right_spaces >= 6
    score = 0
    if data.n >= 6 and data.spaces == 0:
        score = MAXINT
    elif data.n + data.spaces + data.left_spaces + data.right_spaces < 6:
            score = 0
    elif data.n >= 4:
        if data.spaces <= 2:
            score = 2
        elif data.spaces <= 4:
            score = 1
    elif data.n >= 2:
        if data.spaces <= 2:
            score = 1
    
    if color == my_color:
        if score > 0:
            board_score.my_frees += (free_left + free_right)
        if score == 1:
            board_score.possible_safety += 1
        if score == 2:
            board_score.safety += 1
        if score == MAXINT:
            # print("WIN")
            board_score.win += 1
    else:
        if score > 0:
            board_score.opponent_frees += (free_left + free_right)
        if score == 1:
            board_score.possible_threats += 1
        if score == 2:
            board_score.threats += 1
        if score == MAXINT:
            # print("LOSE")
            board_score.lose += 1
    return board_score