import time


from defines import *
from hot_board import update_hot_board, update_remember, calculate_combination_value


def init_board():
    board = np.zeros((GRID_NUM, GRID_NUM), dtype=int)
    # Set borders to BORDER
    board[0][:] = board[:][0] = board[-1][:] = board[:][-1] = BORDER
    
    # Set inner grid to NOSTONE
    board[1:-1][1:-1] = NOSTONE
    return board

# Point (x, y) if in the valid position of the board.
def is_valid_pose(x,y):
    return x > 1 and x < GRID_NUM - 2 and y > 1 and y < GRID_NUM - 2


def make_move(board, bdata, move, color, store=True, true_make=True):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color
    if true_make:
        for m in move.positions:
            bdata.true_board.append((m.x, m.y))
    if store:
        update_remember(bdata, move, True)
    # update_hot_board(board, bdata)


def unmake_move(board, bdata, move):
    board[move.positions[0].x][move.positions[0].y] = NOSTONE
    board[move.positions[1].x][move.positions[1].y] = NOSTONE
    update_remember(bdata, move, False)
    # update_hot_board(board, bdata)


def write_hot_board(hot_board):
    board = [ [0]*(GRID_NUM) for i in range((GRID_NUM))]
    for i in range(21):
        board[i][0] = board[0][i] = board[i][GRID_NUM - 1] = board[GRID_NUM - 1][i] = BORDER
    for i in range(1, GRID_NUM - 1):
        for j in range(1, GRID_NUM - 1):
            board[i][j] = NOSTONE
    for position in hot_board:
        board[position[1]][GRID_NUM - 1 -position[0]] = 'X'
    with open("hot_board.txt", "w") as file:
        for row in board:
            file.write(' '.join(map(str, row)) + '\n')
        for move in hot_board:
            file.write(str(move)+':')
            # for m in hot_board[move]:
            #     file.write(' ' + str(m))
            file.write("\n")
        file.write("\n")


from calculation_module import evaluate_board
def future_score(board, color, my_color, weights, moves):
    for move in moves.positions:
        board[move.x][move.y] = color
    return evaluate_board(board, my_color, weights)


def is_win(board, moves, color):
    directions = np.array([(0, 1), (1, 0), (1, 1), (1, -1)])
    for move in moves.positions:
       for direction in directions:
           count = 1
           add_pos = np.array([-1, 1])
           while len(add_pos) > 0:
                pos = add_pos[0]
                add_pos = np.delete(add_pos, 0)
                # Calculate current cordinates
                row = move.x + direction[0] * pos
                col = move.y + direction[1] * pos
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] == color:
                    count += 1
                    if pos > 0:
                        add_pos = np.append(add_pos, pos + 1)
                    else:
                        add_pos = np.append(add_pos, pos - 1)
                
                if count >= 6:
                    return True
    return False

    if calculate_combination_value(board, move.combination(), color, None) == MAXINT:
        return True
    return False


import numpy as np
def is_win_by_premove(board, preMove):

    directions = np.array([(1, 0), (0, 1), (1, 1), (1, -1)])

    for direction in directions:
        for i in range(len(preMove.positions)):
            count = 0
            position = preMove.positions[i]
            n = x = position.x
            m = y = position.y
            if not is_valid_pose(n, m):
                continue
            actual_move = board[n][m]
            
            if (actual_move == BORDER or actual_move == NOSTONE):
                return False
                
            while board[x][y] == actual_move:
                x += direction[0]
                y += direction[1]
                count += 1
            x = n - direction[0] * count
            y = m - direction[1] * count
            while board[x][y] == actual_move:
                x -= direction[0]
                y -= direction[1]
                count += 1
            if count >= 6:
                return True
    return False


def check_full(board):
    if not np.all(board != 0):
        return False
    else:
        return True


def get_msg(max_len):
    buf = input().strip()
    return buf[:max_len]


def log_to_file(msg):
    g_log_file_name = LOG_FILE
    try:
        with open(g_log_file_name, "a") as file:
            tm = time.time()
            ptr = time.ctime(tm)
            ptr = ptr[:-1]
            file.write(f"[{ptr}] - {msg}\n")
        return 0
    except Exception as e:
        print(f"Error: Can't open log file - {g_log_file_name}")
        return -1


def move2msg(move):
    if move.positions[0].x == move.positions[1].x and move.positions[0].y == move.positions[1].y:
        msg = f"{chr(ord('S') - move.positions[0].x + 1)}{chr(move.positions[0].y + ord('A') - 1)}"
        return msg
    else:
        msg = f"{chr(move.positions[0].y + ord('A') - 1)}{chr(ord('S') - move.positions[0].x + 1)}" \
              f"{chr(move.positions[1].y + ord('A') - 1)}{chr(ord('S') - move.positions[1].x + 1)}"
        return msg


def msg2move(msg):
    move = StoneMove()
    if len(msg) == 2:
        move.positions[0].x = move.positions[1].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = move.positions[1].y = ord(msg[0]) - ord('A') + 1
        move.score = 0
        return move
    else:
        move.positions[0].x = ord('S') - ord(msg[1]) + 1
        move.positions[0].y = ord(msg[0]) - ord('A') + 1
        move.positions[1].x = ord('S') - ord(msg[3]) + 1
        move.positions[1].y = ord(msg[2]) - ord('A') + 1
        move.score = 0
        return move


def write_board_to_file(filename, board, preMove=None):
    with open(filename, 'w') as file:
        file.write("   " + "".join([chr(i + ord('A') - 1) + " " for i in range(1, GRID_NUM - 1)]) + "\n")
        for i in range(1, GRID_NUM - 1):
            file.write(f"{chr(ord('A') - 1 + i)} ")
            for j in range(1, GRID_NUM - 1):
                x = GRID_NUM - 1 - j
                y = i
                stone = board[x][y]
                if stone == NOSTONE:
                    file.write(" -")
                elif stone == BLACK:
                    file.write(" O")
                elif stone == WHITE:
                    file.write(" *")
            file.write(" " + f"{chr(ord('A') - 1 + i)}\n")
        file.write("   " + "".join([chr(i + ord('A') - 1) + " " for i in range(1, GRID_NUM - 1)]) + "\n")


def print_board(board, preMove=None):
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, GRID_NUM - 1)]))
    for i in range(1, GRID_NUM - 1):
        print(f"{chr(ord('A') - 1 + i)}", end=" ")
        for j in range(1, GRID_NUM - 1):
            x = GRID_NUM - 1 - j
            y = i
            stone = board[x][y]
            if stone == NOSTONE:
                print(" -", end="")
            elif stone == BLACK:
                print(" O", end="")
            elif stone == WHITE:
                print(" *", end="")
        print(" ", end="")        
        print(f"{chr(ord('A') - 1 + i)}", end="\n")
    print("   " + "".join([chr(i + ord('A') - 1)+" " for i in range(1, GRID_NUM - 1)]))

def print_score(move_list, n):
    board = [[0] * GRID_NUM for _ in range(GRID_NUM)]
    for move in move_list:
        board[move.x][move.y] = move.score

    print("  " + "".join([f"{i:4}" for i in range(1, GRID_NUM - 1)]))
    for i in range(1, GRID_NUM - 1):
        print(f"{i:2}", end="")
        for j in range(1, GRID_NUM - 1):
            score = board[i][j]
            if score == 0:
                print("   -", end="")
            else:
                print(f"{score:4}", end="")
        print()


def my_print(msg, name):
    with open(name, 'a+') as f:
        tm = time.time()
        ptr = time.ctime(tm)
        ptr = ptr[:-1]
        f.write(f"[{ptr}] - {msg}\n")
    f.close()

"""
    Function to calculate score for one position
    Score is evaluated by the number of stones connected for each direction.
    Score will be MAXINT if same color reach 6 connected or opponenct color reaches 4 (next move could be lost)
    params:
        - board: list with current stones layout
        - move: tuple (x, y) with position to evaluate
        - color: WHITE or BLACK current player
"""
def calculate_single_score(board: np.array, move: tuple, color: int):
    # All directions to check
    directions = np.array([(0, 1), (1, 0), (1, 1), (1, -1)])
    # Dictionary to store scores
    d = {
        'total': 0,
        (0, 1): {WHITE: 0, BLACK: 0},
        (1, 0): {WHITE: 0, BLACK: 0},
        (1, 1): {WHITE: 0, BLACK: 0},
        (1, -1): {WHITE: 0, BLACK: 0}
    }
    # Iterate over all directions
    for direction in directions:
        direction = tuple(direction)
        # Increment array to check all interesing positions
        add_pos = np.array([-1, 1])
        # Same color starts with count 1, itself
        d[direction][color] = 1
        while len(add_pos) > 0:
            # Get first element, queue behavior
            pos = add_pos[0]
            add_pos = np.delete(add_pos, 0)
            # Calculate current cordinates
            row = move[0] + direction[0] * pos
            col = move[1] + direction[1] * pos
            # Pass outlimits positions
            if not is_valid_pose(row, col):
                continue
            # If there is any stone
            current_color = board[row][col]
            if current_color != NOSTONE:
                # Increase the corresponding counter
                d[direction][current_color] += 1
                # Check next position in same direction and sign
                if pos > 0:
                    add_pos = np.append(add_pos, pos + 1)
                else:
                    add_pos = np.append(add_pos, pos - 1)
                # Check win or opponent win to increase rating
                if d[direction][current_color] >= 6 - (0 if current_color == color else 2):
                    d[direction][current_color] = MAXINT
        # Add total count
        d['total'] += d[direction][WHITE] + d[direction][BLACK]

    return d
