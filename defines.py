GRID_NUM = 21               # Number of the board, 19*19 plus edges.
GRID_COUNT = 361            # Sum of the points in the board.
BLACK = 1                   # Black flag in the board.
WHITE = 2                   # White flag in the board.
BORDER = 3                  # Border flag in the board.
NOSTONE = 0                 # Empty flag.
MSG_LENGTH = 512            #Tamaño del mensaje
GRID_COUNT = 361            #Sum of the points in the board.
LOG_FILE = "tia-engine.log"
ENGINE_NAME = "TIA.Connect6"
# Max values in the evaluation.
MAXINT = 20000
MININT = -20000
DEPTH = 1

HOT_IMPACT = 1


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

    # Function to print StoneMove data
    def __str__(self):
        return f"{self.positions[0]} : {self.positions[1]}"


# One point and its value.
class Chess:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score


class AlphaBeta:
    def __init__(self, alpha = MININT, beta = MAXINT):
        self.alpha = alpha
        self.beta = beta
    
    """
        Returns True if alpha is greater than beta, so stop expanding
    """
    def __bool__(self):
        return self.alpha >= self.beta