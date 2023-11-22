from defines import *
import numpy as np


"""
    Function to update hot board data. Create a dictionary with just interesing positions
    Params:
        - board: numpy array with current board layout
        - bdata: Bdata object that stores all variables such as hot_board, true_board...
    Returns:
        None
"""
def update_hot_board(board: np.array, bdata: BData):
    # Reset dictionary
    hot_board = []
    # Iterate over all remembered movements
    for moves in bdata.remembered_moves['queue']:
        # Each movement is composed by 2 stone positions
        for move in moves.positions:
            # Delete current position in hot board as it cannot be a possible move
            if (move.x, move.y) in hot_board:
                hot_board.remove((move.x, move.y))
            # Go through all postions that could be imapcted by current move
            """
                *  *  *
                  ***
                * *O* *
                  ***
                *  *  *
            """
            for row in range(move.x - HOT_IMPACT, move.x + HOT_IMPACT + 1):
                for col in get_values(move.y - 2, move.y + 2, row - move.x):
                    # Pass current position as it cannot be in hot_board
                    if row == move.x and col == move.y:
                        continue
                    # Pass outlimits positions
                    if not is_valid_pose(row, col):
                        continue
                    # If there is a stone in positions
                    if board[row][col] != NOSTONE:
                        # And is present in hot_board, delete
                        if (row, col) in hot_board:
                            hot_board.remove((row, col))
                        continue
                    # Create position 
                    if not (row, col) in hot_board:
                        hot_board.append((row, col))
    # For each move in true board
    for move in bdata.true_board:
        # Check if there is any crucial move to not forget it
        check_persistant(board, hot_board, StonePosition(move[0], move[1]))

    bdata.hot_board = np.array(hot_board)


"""
    Function to update lists for remembered moves and stored moves
    params:
        - bdata: Bdata object that stores all variables such as remembered_moves
        - moves: StoneMove object with currente move to update in lists
        - make: bool variable
            * True: new move
            * False: delete move
"""
def update_remember(bdata: BData, moves: StoneMove, make: bool):
    if make:
        # Add current move to remebered moves if it is not already present
        if not moves in bdata.remembered_moves['queue']:
            bdata.remembered_moves['queue'].append(moves)
        # If currente rembeber queue is bigger than fixed memory 
        if len(bdata.remembered_moves['queue']) > MOVEMENTS_MEMORY:
            # Get first move (older one)
            lost_move = bdata.remembered_moves['queue'][0]
            # Append to last position in discarded stack
            bdata.remembered_moves['discarded_queue'].append(lost_move)
            # Remove from remeber list
            bdata.remembered_moves['queue'] = bdata.remembered_moves['queue'][1:]
    else:
        # If current move is last recorded in queue
        if bdata.remembered_moves['queue'][-1] == moves:
            # Delete last position in rembebered queue
            bdata.remembered_moves['queue'] = bdata.remembered_moves['queue'][:-1]
            # If there is any discard
            if bdata.remembered_moves['discarded_queue']:
                # Get last position of stack and append it to remembered positions
                bdata.remembered_moves['queue'] = bdata.remembered_moves['discarded_queue'][-1:] + bdata.remembered_moves['queue']
                bdata.remembered_moves['discarded_queue'] = bdata.remembered_moves['discarded_queue'][:-1]


# Point (x, y) if in the valid position of the board.
def is_valid_pose(x,y):
    return x > 0 and x < GRID_NUM - 1 and y > 0 and y < GRID_NUM - 1


"""
    Function to create column iterable list based on row to create gemoetric influence
    *  *  *
      ***
    * *O* *
      ***
    *  *  *
"""
def get_values(minimum, maximum, row):
    if abs(row) == 1:
        return range(minimum + 1, maximum)
    if abs(row) == 2:
        return range(minimum, maximum + 1, 2)
    else:
        return range(minimum, maximum + 1)


"""
    Function to ponderate movement based on nearby stones and possible wins
    params:
        - board: current stone layout
        - combination:
        - color: WHITE or BLACK define
        - score_chess: dictionary with keys as point coorinates and value as score for each direaction for each color
        - maximum: list with one int to modify its value inside function
    returns:
        - score: int with combination rating
"""
def calculate_combination_value(
        board: np.array,
        combination,
        color: int,
        score_chess: dict,
        maximum: list = None):
    # Get direction influence between stones
    direction = check_influence(combination)
    # If no there is no influence, return sum of individual scores
    if direction == 0:
        return score_chess[tuple(combination[0])]['total'] + score_chess[tuple(combination[1])]['total']
    future_board = np.copy(board)

    moves = StoneMove(combination).positions
    # Create move in a copy of board
    score = 0
    # Create moves in board and get scores of the rest of directions
    for move in moves:
        if future_board[move.x][move.y] == NOSTONE:
            future_board[move.x][move.y] = color
        score += sum(
            [score_chess[(move.x, move.y)][v][BLACK] + score_chess[(move.x, move.y)][v][WHITE] if v != direction
            else 0
            for v in [(0, 1), (1, 0), (1, 1), (1, -1)]]
        )
    last = color
    # Start counting for each color starting if color is same
    black_count = BLACK == color
    white_count = WHITE == color
    # Increment array to check all interesing positions
    add_pos = np.array([-1, 1])
    while len(add_pos) > 0:
        # Get first element, queue behavior
        pos = add_pos[0]
        add_pos = np.delete(add_pos, 0)
        # Calculate current cordinates
        row = move.x + direction[0] * pos
        col = move.y + direction[1] * pos
        # Pass outlimits positions
        if not is_valid_pose(row, col):
            continue
        # If there is any stone
        if future_board[row][col] != NOSTONE:
            # Increase the corresponding counter
            if future_board[row][col] == WHITE:
                white_count += 1
            else:
                black_count += 1
            if last != color:
                continue
            # Check next position in same direction and sign
            if pos > 0:
                add_pos = np.append(add_pos, pos + 1)
            else:
                add_pos = np.append(add_pos, pos - 1)
        # If any color reach 6 or 4 if it's opponent color, return maximum value
        if black_count >= 6 - (0 if BLACK == color else 2):
            if maximum != None:
                maximum[0] = MAXINT
            return MAXINT
        if white_count >= 6 - (0 if WHITE == color else 2):
            if maximum != None:
                maximum[0] = MAXINT
            return MAXINT
    # Add rating
    score += white_count + black_count
    if maximum != None:
        maximum[0] = max(score, maximum[0])
    return score

"""
    Function to check if 2 positions are aligned in any relevant direction
    params:
        - combination: tuple of tuples with both points coridnates ((x1, y1), (x2, y2))
    returns:
        - tuple with direction influence
        - 0, no influence
"""
def check_influence(combination: tuple):
    # Get all cordinates to simplify code
    x1 = combination[0][0]
    y1 = combination[0][1]
    x2 = combination[1][0]
    y2 = combination[1][1]
    # Get vector between points
    vx = x2 - x1
    vy = y2 - y1
    # Same x value is horizontal direction
    if x1 == x2:
        return (0,1)
    # Same y value is vertical direction
    elif y1 == y2:
        return (1, 0)
    # Same vector components is diagonal (D1) direction
    elif vx == vy:
        return (1, 1)
    # Same module of the vector components is diagonal (D2) direction
    elif vx == -vy:
        return (1, -1)
    # No influence between points
    else:
        return 0



"""
    Function to check if there is any position that could be forgotten and its importart
    params:
        - board: current stone layout
        - hot_board: dictionary with interesting positions
        - move: current move
"""
def check_persistant(board: np.array, hot_board: dict, move: StoneMove):
    # define all directions to search
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # Get current player color
    color = board[move.x][move.y]
    # Itereate over all directions
    for direction in directions:
        count = 1
        check_list = np.array([-1, 1])
        while len(check_list) > 0:
            # Get first element, queue behavior
            pos = check_list[0]
            check_list = check_list[1:]
            # Calculate current cordinates
            row = move.x + direction[0] * pos
            col = move.y + direction[1] * pos
            # Pass outlimits positions
            if not is_valid_pose(row, col):
                continue
            # If stone is same color
            if board[row][col] == color:
                # Add counter
                count += 1
                # Add next 2 positions
                # So when checking last stone, following 2 positions will be added
                if pos > 0:
                    adds = [1, 2]    
                else:
                    adds = [-1, -2]
                for i in adds:
                    if not pos + i in check_list:
                        check_list = np.append(check_list, pos + i)
            elif board[row][col] == color ^ 3:
                if pos > 0:
                    check_list = check_list[check_list < 0]
                else:
                    check_list = check_list[check_list > 0]

            # Current position is empty and there is 4 stone in a row
            if count >= 4 and board[row][col] == NOSTONE:
                # Add interesting position
                if (row, col) not in hot_board:
                    hot_board.append((row, col))
