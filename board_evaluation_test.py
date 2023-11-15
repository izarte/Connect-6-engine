from defines import *
from tools import *
from calculation_module import evaluate_board
from hot_board import calculate_combination_value

import time

board = [ [0]*GRID_NUM for i in range(GRID_NUM)]
hot_board = {}
init_board(board)

# board[10][10] = BLACK
# board[4][1] = BLACK

# board[4][11] = BLACK
# board[4][9] = BLACK


# board[8][10]= BLACK
board[9][10]= BLACK
board[10][10] = BLACK
board[12][10] = BLACK
board[9][9] = WHITE
board[10][9] = WHITE
board[11][9] = WHITE
board[12][9] = WHITE

# board[8][7] = WHITE
# board[8][9] = WHITE
# move = StoneMove(((4, 4), (3, 3)))
# make_move(board, hot_board, move, BLACK)
# board[4][4] = WHITE
# board[3][3] = WHITE

# board[4][2] = BLACK

# board[10][9] = BLACK

print_board(board)
s = calculate_combination_value(board, ((8,9),(13,9)), WHITE)
print(s)
# start = time.perf_counter()
# s = evaluate_board(board, BLACK, [50, 1, -100, -1],True)
# end = time.perf_counter()
# print(f"Score: {s}")
# print(f"Time: {end - start}")

# hot_board = {}
# move = StoneMove(((10, 10), (10, 10)))
# start = time.perf_counter()
# v = make_move(board, hot_board, move, BLACK)
# make = time.perf_counter()
# unmake_move(board, hot_board, move)
# end = time.perf_counter()

# print(f"Value: {v}")
# print(f"Make time: {make - start}, unmake: {end - make}")
