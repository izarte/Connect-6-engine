from defines import *
import numpy as np


def update_hot_board(board, bdata):
    hot_board = {}

    for moves in bdata.remembered_moves['queue']:
        for move in moves.positions:
            if (move.x, move.y) in hot_board:
                del hot_board[(move.x, move.y)]
            for row in range(move.x - HOT_IMPACT, move.x + HOT_IMPACT + 1):
                for col in get_values(move.y - 2, move.y + 2, row - move.x):
                    if row == move.x and col == move.y:
                        continue
                    if not is_valid_pose(row, col):
                        continue
                    if board[row][col] != NOSTONE:
                        if (row, col) in hot_board:
                            del hot_board[(row, col)]
                        continue
                    if not (row, col) in hot_board:
                        hot_board[(row, col)] = [(move.x, move.y)]
                    elif not (move.x, move.y) in hot_board[(row, col)]:
                        hot_board[(row, col)].append((move.x, move.y))

    for move in bdata.true_board:
        check_persistant(board, hot_board, StonePosition(move[0], move[1]))

    bdata.hot_board = hot_board


def update_remember(bdata, moves, make):
    if make:
        if not moves in bdata.remembered_moves['queue']:
            bdata.remembered_moves['queue'].append(moves)
        if len(bdata.remembered_moves['queue']) > 2:
            lost_move = bdata.remembered_moves['queue'][0]
            bdata.remembered_moves['discarded_queue'].append(lost_move)
            bdata.remembered_moves['queue'] = bdata.remembered_moves['queue'][1:]
    else:
        if bdata.remembered_moves['queue'][-1] == moves:
            bdata.remembered_moves['queue'] = bdata.remembered_moves['queue'][:-1]
            if bdata.remembered_moves['discarded_queue']:
                bdata.remembered_moves['queue'] = bdata.remembered_moves['discarded_queue'][-1:] + bdata.remembered_moves['queue']
                bdata.remembered_moves['discarded_queue'] = bdata.remembered_moves['discarded_queue'][:-1]


def get_values(minimum, maximum, row):
    if abs(row) == 1:
        return range(minimum + 1, maximum)
    if abs(row) == 2:
        return range(minimum, maximum + 1, 2)
    else:
        return range(minimum, maximum + 1)


# Point (x, y) if in the valid position of the board.
def is_valid_pose(x,y):
    return x > 0 and x < GRID_NUM - 1 and y > 0 and y < GRID_NUM - 1


def calculate_combination_value(board, combination, color, maximum=None, first=True):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    if isinstance(combination, StoneMove):
        moves = combination.positions
    elif isinstance(combination, StonePosition):
        moves = [combination]
    else:
        moves = StoneMove(combination)
        moves = moves.positions
    score = 0
    future_board = np.copy(board)
    for move in moves:
        if future_board[move.x][move.y] == NOSTONE:
            future_board[move.x][move.y] = color
    for move in moves:
        color = board[move.x][move.y]
        for direction in directions:
            black_count = BLACK == color
            white_count = WHITE == color
            add_pos = np.array([-1, 1])

            while len(add_pos) > 0:
                pos = add_pos[0]
                add_pos = np.delete(add_pos, 0)
                row = move.x + direction[0] * pos
                col = move.y + direction[1] * pos
                if not is_valid_pose(row, col):
                    continue
                if future_board[row][col] != NOSTONE:
                    if future_board[row][col] == WHITE:
                        white_count += 1
                    else:
                        black_count += 1
                        
                    if pos > 0:
                        add_pos = np.append(add_pos, pos + 1)
                    else:
                        add_pos = np.append(add_pos, pos - 1)
                # print(row, col, future_board[row][col], count, add_pos)
                c = 2 if not first else 0
                if black_count >= 6 - (0 if BLACK == color else 2):
                    if maximum != None:
                        maximum[0] = MAXINT
                    return MAXINT
                if white_count >= 6 - (0 if WHITE == color else 2):
                    if maximum != None:
                        maximum[0] = MAXINT
                    return MAXINT
        score += white_count + black_count
    if maximum != None:
        maximum[0] = max(score, maximum[0])
    return score


def check_persistant(board, hot_board, move):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    color = board[move.x][move.y]
    for direction in directions:
        count = 1
        check_list = [-1, 1]
        while len(check_list) > 0:
            pos = check_list[0]
            check_list = check_list[1:]
            row = move.x + direction[0] * pos
            col = move.y + direction[1] * pos
            if not is_valid_pose(row, col):
                continue
            
            if board[row][col] == color:
                count += 1
                if pos > 0:
                    adds = [1, 2]    
                else:
                    adds = [-1, -2]
                for i in adds:
                    if not pos + i in check_list:
                        check_list.append(pos + i)
            if count >= 4 and board[row][col] == NOSTONE:
                hot_board[(row, col)] = [(row, col)]
