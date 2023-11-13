from defines import *
from tools import *
from calculation_module import evaluate_board

import time

board = [ [0]*GRID_NUM for i in range(GRID_NUM)]
hot_board = {}
init_board(board)

# board[10][10] = BLACK
# board[4][1] = BLACK

# board[4][11] = BLACK
board[4][9] = BLACK


board[8][8] = BLACK
board[7][7] = BLACK
board[6][6] = BLACK
board[5][5] = BLACK

# move = StoneMove(((4, 4), (3, 3)))
# make_move(board, hot_board, move, BLACK)
# board[4][4] = WHITE
# board[3][3] = WHITE

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
