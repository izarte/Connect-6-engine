from defines import *
import time

# Point (x, y) if in the valid position of the board.
def is_valid_pose(x,y):
    return x > 0 and x < GRID_NUM - 1 and y > 0 and y < GRID_NUM - 1
    
def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][GRID_NUM - 1] = board[GRID_NUM - 1][i] = BORDER
    for i in range(1, GRID_NUM - 1):
        for j in range(1, GRID_NUM - 1):
            board[i][j] = NOSTONE
            
def make_move(board, hot_board: dict, move, color):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color
    update_hot_board(hot_board, board, move, make=True)


def unmake_move(board, hot_board, move):
    board[move.positions[0].x][move.positions[0].y] = NOSTONE
    board[move.positions[1].x][move.positions[1].y] = NOSTONE
    update_hot_board(hot_board, board, move, make=False)


"""
    make = True if is maken move, False if is unmaken
"""
def update_hot_board(hot_board: dict, board, moves: StoneMove, make: bool):
    counter = 0
    for move in moves.positions:
        # If make action and position is in hot_board, delete it
        if make and (move.x, move.y) in hot_board:
            del hot_board[(move.x, move.y)]
        # Go through all the neighbors
        for row in range(move.x - HOT_IMPACT, move.x + HOT_IMPACT + 1):
            for col in range(move.y - HOT_IMPACT, move.y + HOT_IMPACT + 1):
                # If current iteration is move, ignore
                if make and row == move.x and col == move.y:
                    continue
                # If current position is outside board limits, ignore
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] != NOSTONE: # If there's already a stone in the main board, ignore
                    continue
                target = StonePosition(row, col)
                impact = StonePosition(move.x, move.y)
                # Unmake action. Unmaken move should be hot
                if not make:
                    target = StonePosition(move.x, move.y)
                    impact = StonePosition(row, col)
                    if (row, col) in hot_board:
                        if (move.x, move.y) in hot_board[(row, col)]:
                            # my_print(f"DELETED {row}, {col} by {move}", "log.txt")
                            hot_board[(row, col)].remove((move.x, move.y))
                        if not hot_board[(row, col)]:
                            del hot_board[(row, col)]
                if not (target.x, target.y) in hot_board: # If the hot position is not already created, create hot position
                    # my_print(f"CREATED {target} by {impact}", "log.txt")
                    hot_board[(target.x, target.y)] = [(impact.x, impact.y)]
                    counter += 1
                    continue
                if not (impact.x, impact.y) in hot_board[(target.x, target.y)]:# If it already exists, append actual position to store impact in the same hot position
                    hot_board[(target.x, target.y)].append((impact.x, impact.y))
                    # my_print(f"ADD {target} by {impact}", "log.txt")
    return counter


# Calculate hot_board impact for a move
def calculate_combination_value(board, hot_board, combination):
    value = 0
    for move in combination:
        for row in range(move[0] - HOT_IMPACT, move[0] + HOT_IMPACT + 1):
            for col in range(move[1] - HOT_IMPACT, move[1] + HOT_IMPACT + 1):
                if not is_valid_pose(row, col):
                    continue
                if board[row][col] != NOSTONE:
                    value += 1
    # move = StoneMove(combination)
    # value = update_hot_board(hot_board, board, move, make = True)
    # update_hot_board(hot_board, board, move, make = False)
    return value



def write_hot_board(hot_board):
    board = [ [0]*(GRID_NUM) for i in range(GRID_NUM)]
    init_board(board)
    for position in hot_board:
        board[position[1]][GRID_NUM - 1 -position[0]] = 'X'
    with open("hot_board.txt", "w") as file:
        for row in board:
            file.write(' '.join(map(str, row)) + '\n')
        for move in hot_board:
            file.write(str(move)+':')
            for m in hot_board[move]:
                file.write(' ' + str(m))
            file.write("\n")
        file.write("\n")


def is_win_by_premove(board, preMove):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for direction in directions:
        for i in range(len(preMove.positions)):
            count = 0
            position = preMove.positions[i]
            n = x = position.x
            m = y = position.y
            actual_move = board[n][m]
            
            if (actual_move == BORDER or actual_move == NOSTONE):
                return False
                
            while board[x][y] == actual_move:
                x += direction[0]
                y += direction[1]
                count += 1
            x = n - direction[0]
            y = m - direction[1]
            while board[x][y] == actual_move:
                x -= direction[0]
                y -= direction[1]
                count += 1
            if count >= 6:
                return True
    return False

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