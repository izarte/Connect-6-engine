from defines import *
from tools import *
from calculation_module import evaluate_board

import time

board = [ [0]*GRID_NUM for i in range(GRID_NUM)]

init_board(board)

# board[10][10] = BLACK
# board[4][1] = BLACK
board[4][16] = BLACK
board[4][8] = WHITE
board[4][7] = WHITE
board[4][6] = WHITE
board[4][5] = WHITE
# board[10][9] = BLACK

print_board(board)
start = time.perf_counter()
s = evaluate_board(board, BLACK)
end = time.perf_counter()
print(f"Score: {s}")
print(f"Time: {end - start}")