from defines import *

def make_hot_board(hot_board: dict, board, true_board, remembered_moves, moves: StoneMove, store):
    if store and not moves in remembered_moves['queue']:
        remembered_moves['queue'].append(moves)
    for move in moves.positions:
        if (move.x, move.y) in hot_board:
            del hot_board[(move.x, move.y)]
        for row in range(move.x - HOT_IMPACT, move.x + HOT_IMPACT + 1):
            for col in get_values(move.y - 2, move.y + 2, row - move.x):
            # for col in range(move.y - HOT_IMPACT, move.y + HOT_IMPACT + 1):
                if row == move.x and col == move.y:
                    continue
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] != NOSTONE:
                    if (row, col) in hot_board:
                        del hot_board[(row, col)]
                    continue
                make_persistant(board, hot_board, true_board, move, row, col)
                if not (row, col) in hot_board:
                    hot_board[(row, col)] = [(move.x, move.y)]
                elif not (move.x, move.y) in hot_board[(row, col)]:
                    hot_board[(row, col)].append((move.x, move.y))
    if len(remembered_moves['queue']) > 2:
        lost_move = remembered_moves['queue'][0]
        remembered_moves['discarded_queue'].append(lost_move)
        remembered_moves['queue'] = remembered_moves['queue'][1:]
        unmake_hot_board(hot_board, board, true_board, remembered_moves, lost_move, False)


def make_persistant(board, hot_board, true_board, move, p_row, p_col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # for move in moves.positions:
    if not (move.x, move.y) in true_board:
        return
    color = board[move.x][move.y]
    for direction in directions:
        count = 0
        add_pos = [-1, 1]
        check = True
        while len(add_pos) > 0:
            pos = add_pos[0]
            add_pos = add_pos[1:]
            row = p_row + direction[0] * pos
            col = p_col + direction[1] * pos
            if not is_valid_pose(row, col):
                continue

            if count >= 4:
                if check:
                    check = False
                    add_pos.append(0)

                print(move, row, col)
                hot_board[(row, col)] = [(row, col)]
            
            if board[row][col] == color:
                count += 1
                if pos > 0:
                    add_pos.append(pos + 1)
                else:
                    add_pos.append(pos - 1)
            elif board[row][col] != NOSTONE:
                continue



def unmake_hot_board(hot_board: dict, board, true_board, remembered_moves, moves: StoneMove, restore=True):
    nec = False
    for move in moves.positions:
        if not (move.x, move.y) in hot_board:
            nec = True
        for row in range(move.x - HOT_IMPACT, move.x + HOT_IMPACT + 1):
            # for col in range(move.y - HOT_IMPACT, move.y + HOT_IMPACT + 1):
            for col in get_values(move.y - 2, move.y + 2, row - move.x):
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] != NOSTONE:
                    continue
                if (row, col) in hot_board:
                    if (move.x, move.y) in hot_board[(row, col)]:

                        hot_board[(row, col)].remove((move.x, move.y))
                    if not hot_board[(row, col)]:

                        del hot_board[(row, col)]
                if nec:
                    if board[row][col] == BLACK or board[row][col] == WHITE:
                        make_persistant(board, hot_board, true_board, StonePosition(row, col), move.x, move.y)
                        if not (move.x, move.y) in hot_board:
                            hot_board[(move.x, move.y)] = [(row, col)]
                        else:
                            hot_board[(move.x, move.y)].append((row, col))

    if restore and remembered_moves['queue'][-1] == moves:
        remembered_moves['queue'] = remembered_moves['queue'][:-1]
        if remembered_moves['discarded_queue']:
            restore_move = remembered_moves['discarded_queue'][-1]
            remembered_moves['queue'] = remembered_moves['discarded_queue'][-1:] + remembered_moves['queue']
            remembered_moves['discarded_queue'] = remembered_moves['discarded_queue'][:-1]
            make_hot_board(hot_board, board, [], remembered_moves, restore_move, False)


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


def calculate_combination_value(board, combination):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    if isinstance(combination, StoneMove):
        moves = combination.positions
    elif isinstance(combination, StonePosition):
        moves = [combination]
    else:
        moves = StoneMove(combination)
        moves = moves.positions
    score = 0
    for move in moves:
        for direction in directions:
            count = 0
            add_pos = [-1, 1]
            while len(add_pos) > 0:
                pos = add_pos[0]
                add_pos = add_pos[1:]
                row = move.x + direction[0] * pos
                col = move.y + direction[1] * pos
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] != NOSTONE:
                    count += 1
                    if pos > 0:
                        add_pos.append(pos + 1)
                    else:
                        add_pos.append(pos - 1)
                if count >= 3:
                    return MAXINT
        score += count

    return score
