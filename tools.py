import time


from defines import *
from hot_board import update_hot_board, update_remember, calculate_combination_value
# from update_hot_board import update_hot_board


def init_board(board):
    for i in range(21):
        board[i][0] = board[0][i] = board[i][GRID_NUM - 1] = board[GRID_NUM - 1][i] = BORDER
    for i in range(1, GRID_NUM - 1):
        for j in range(1, GRID_NUM - 1):
            board[i][j] = NOSTONE


def make_move(board, bdata, move, color, store=True, true_make=True):
    board[move.positions[0].x][move.positions[0].y] = color
    board[move.positions[1].x][move.positions[1].y] = color
    if true_make:
        for m in move.positions:
            bdata.true_board.append((m.x, m.y))
    if store:
        update_remember(bdata, move, True)
    # t = time.perf_counter()
    update_hot_board(board, bdata)
    # print(f"T: {time.perf_counter() - t}")
    # print("TRUE: ", bdata.true_board)
    # write_hot_board(bdata.hot_board)
    # print_board(board)
    # input()
    # make_hot_board(hot_board=hot_board, board=board, true_board=true_board, moves=move, remembered_moves=remembered_moves, store=store)


def unmake_move(board, bdata, move):
    board[move.positions[0].x][move.positions[0].y] = NOSTONE
    board[move.positions[1].x][move.positions[1].y] = NOSTONE
    # for m in move.positions:
    #     future_moves.remove((m.x, m.y))
    update_remember(bdata, move, False)
    # t = time.perf_counter()
    update_hot_board(board, bdata)
    # print(f"T: {time.perf_counter() - t}")
    # unmake_hot_board(hot_board=hot_board, board=board, true_board=true_board, moves=move, remembered_moves=remembered_moves)


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

def is_win_or_will_be_win(board, move):
    if calculate_combination_value(board, move, BLACK, None, True) == MAXINT:
        return True
    if calculate_combination_value(board, move, WHITE, None, True) == MAXINT:
        return True
    return False


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


def check_full(board):
    for row in board:
        if 0 in row:
            return False
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
