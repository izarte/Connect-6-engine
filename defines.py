import numpy as np

GRID_NUM = 21               # Number of the board, 19*19 plus edges.
GRID_COUNT = 361            # Sum of the points in the board.
BLACK = 1                   # Black flag in the board.
WHITE = 2                   # White flag in the board.
BORDER = 3                  # Border flag in the board.
NOSTONE = 0                 # Empty flag.
MSG_LENGTH = 512            # Tamaño del mensaje
GRID_COUNT = 361            # Sum of the points in the board.
LOG_FILE = "tia-engine.log"
ENGINE_NAME = "TIA.Connect6"
# Max values in the evaluation.
MAXINT = 20000
MININT = -20000
DEPTH = 3

HOT_IMPACT = 2
MOVEMENTS_MEMORY = 2


class StonePosition:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"{self.x}, {self.y}"

class StoneMove:
    # Move equals None to make it unecessary but if present fill values
    # Move if not none will be a tuple of 2 tuples as ((x1, y1), (x2, y2))
    def __init__(self, move = None):
        first_move = StonePosition(0, 0)
        second_move = StonePosition(0, 0)
        if move:
            first_move.x = move[0][0]
            first_move.y = move[0][1]
            second_move.x = move[1][0]
            second_move.y = move[1][1]

        self.positions = [first_move, second_move]
        self.score = 0
    
    def combination(self):
        return ((self.positions[0].x, self.positions[0].y), (self.positions[1].x, self.positions[1].y))

    # Function to print StoneMove data
    def __str__(self):
        return f"{self.positions[0]} : {self.positions[1]}"



# One point and its value.
class CombinationScore:
    def __init__(self, vals, score):
        self.x1 = vals[0][0]
        self.y1 = vals[1][0]
        self.x2 = vals[0][1]
        self.y2 = vals[1][1]
        self.score = score
    
    def values(self):
        return ((self.x1, self.y1), (self.x2, self.y2))
    
    def __str__(self):
        return f"{self.x1} {self.y1} - {self.x2} {self.y2} {self.score}"


class AlphaBeta:
    def __init__(self, alpha = MININT, beta = MAXINT):
        self.alpha = alpha
        self.beta = beta
    
    """
        Returns True if alpha is greater than beta, so stop expanding
    """
    def __bool__(self):
        return self.alpha >= self.beta

"""
    Class to store data
    values:
        - hot_board: dict with interesting positions for next search
        - true_board: list with positions made by any of player
        - remembered_mmoves: dict to store move that algorithm will remember
            * queue: list to imitate queue (FIFO) to store movements to remember
            * discarded_queue: list to imitate stack (LIFO) to store 
                forgotten movements to restore when needed
"""
class BData():
    def __init__(self):
        self.hot_board = []
        self.true_board = []
        self.remembered_moves = {'queue': [], 'discarded_queue': []}

    def print_remember(self):
        for m in self.remembered_moves['queue']:
            print(m, end=' - ')
        print("discarded: ", end='')
        for m in self.remembered_moves['discarded_queue']:
            print(m, end=' - ')
        print()