import time
from defines import *
from tools import init_board, check_full, make_move, is_win, my_print


def get_metrics(search_function):
    t = time.perf_counter()
    board = init_board()
    bdata = {
        BLACK: BData(),
        WHITE: BData() 
    }
    move = StoneMove()
    color = BLACK
    tournament_data = {
        BLACK: {'color': color, 'board' : board, 'bdata': bdata, 'weights': []},
        WHITE: {'color': color, 'board' : board, 'bdata': bdata, 'weights': []}
    }
    i = 0
    weights = []
    data = []
    while not check_full(board) and not is_win(board, move, color) and i < 20:
        color = color ^ 3
        tournament_data[color]['color'] = color
        tournament_data[color]['board'] = board
        tournament_data[color]['bdata'] = bdata[color]
        tournament_data[color]['weights'] = weights
        move, t, nodes = search_function(color, move, weights, tournament_data=tournament_data[color], return_metrics=True)
        data.append([t, nodes])
        make_move(board, bdata[color], move, color)
        make_move(board, bdata[color ^ 3], move, color)
        i += 1
    write_csv(data)

import csv
def write_csv(data):
    with open("data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerows(data)