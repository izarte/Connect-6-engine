from defines import *
from tools import *
from calculation_module import evaluate_board

import time

board = [ [0]*GRID_NUM for i in range(GRID_NUM)]

init_board(board)

# board[10][10] = BLACK
# board[4][1] = BLACK

# board[4][11] = BLACK
board[4][9] = BLACK


board[4][8] = WHITE
board[4][7] = WHITE
board[4][6] = WHITE
board[4][5] = WHITE
board[4][4] = WHITE
board[4][3] = WHITE

board[4][2] = BLACK

# board[10][9] = BLACK

print_board(board)
start = time.perf_counter()
s = evaluate_board(board, BLACK)
end = time.perf_counter()
print(f"Score: {s}")
print(f"Time: {end - start}")

# hot_board = {}
# move = StoneMove(((10, 10), (10, 10)))
# start = time.perf_counter()
# v = make_move(board, hot_board, move, BLACK)
# make = time.perf_counter()
# unmake_move(board, hot_board, move)
# end = time.perf_counter()

# print(f"Value: {v}")
# print(f"Make time: {make - start}, unmake: {end - make}")
