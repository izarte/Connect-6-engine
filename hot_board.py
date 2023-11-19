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
    hot_board = {}
    # Iterate over all remembered movements
    for moves in bdata.remembered_moves['queue']:
        # Each movement is composed by 2 stone positions
        for move in moves.positions:
            # Delete current position in hot board as it cannot be a possible move
            if (move.x, move.y) in hot_board:
                del hot_board[(move.x, move.y)]
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
                            del hot_board[(row, col)]
                        continue
                    # Create position 
                    if not (row, col) in hot_board:
                        hot_board[(row, col)] = [(move.x, move.y)]
                    elif not (move.x, move.y) in hot_board[(row, col)]:
                        hot_board[(row, col)].append((move.x, move.y))
    # For each move in true board
    for move in bdata.true_board:
        # Check if there is any crucial move to not forget it
        check_persistant(board, hot_board, StonePosition(move[0], move[1]))

    bdata.hot_board = hot_board

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


# Point (x, y) if in the valid position of the board.
def is_valid_pose(x,y):
    return x > 0 and x < GRID_NUM - 1 and y > 0 and y < GRID_NUM - 1

"""
    Function to ponderate movement based on nearby stones and possible wins
    params:
        - board: current stone layout
        - combination:
        - color: WHITE or BLACK define
        - maximum: list with one int to modify its value inside function
    returns:
        - score: int with combination rating
"""
def calculate_combination_value(
        board: np.array,
        combination,
        color: int,
        maximum: list = None):

    # define all directions to search
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # Unify different possible input combination type
    if isinstance(combination, StoneMove):
        moves = combination.positions
    elif isinstance(combination, StonePosition):
        moves = [combination]
    else:
        moves = StoneMove(combination)
        moves = moves.positions
    score = 0
    future_board = np.copy(board)
    # Create move in a copy of board
    for move in moves:
        if future_board[move.x][move.y] == NOSTONE:
            future_board[move.x][move.y] = color
    # iterate over each stone position
    for move in moves:
        # Get color of move
        color = future_board[move.x][move.y]
        # Itereate over all directions
        for direction in directions:
            # Start counting for each color starting if color is same
            black_count = BLACK == color
            white_count = WHITE == color
            # Increment array to check all interesing positions
            add_pos = np.array([-1, 1])

            while len(add_pos) > 0:
                # Get fist element, queue behavior
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
    # Update maximum value
    if maximum != None:
        maximum[0] = max(score, maximum[0])
    return score

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
            # Current position is empty and there is 4 stone in a row
            if count >= 4 and board[row][col] == NOSTONE:
                # Add interesting position
                hot_board[(row, col)] = [(row, col)]
