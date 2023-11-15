from defines import *
from tools import init_board, write_hot_board, make_move
from hot_board import update_hot_board, make_persistant



if __name__ == '__main__':
    board = [ [0]*GRID_NUM for i in range(GRID_NUM)]
    bdata = BData()
    init_board(board)

    move = StoneMove(((10, 10), (10, 10)))
    make_move(board, bdata, move, BLACK)
    move = StoneMove(((10, 11), (10, 9)))
    make_move(board, bdata, move, BLACK)
    # move = StoneMove(((8, 8), (11, 10)))
    # make_move(board, hot_board, move, BLACK, remembered_moves)
    # move = StoneMove(((9, 9), (11, 9)))
    # make_move(board, hot_board, move, BLACK, remembered_moves)
    
    # unmake_move(board, hot_board,remembered_moves, move)

    # move = StoneMove(((9, 9), (11, 9)))
    # make_move(board, hot_board, move, BLACK, remembered_moves)


    # unmake_move(board, hot_board,remembered_moves, move)

    write_hot_board(bdata.hot_board)