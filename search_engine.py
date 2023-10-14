from tools import *
from tree import TreeNode


class SearchEngine():
    def __init__(self):
        self.board = None
        self.chess_type = None
        self.alphabeta_depth = None
        self.total_nodes = 0

    def update_parameters(self, board, hot_board, color, alphabeta_depth):
        self.board = board
        self.hot_board = hot_board
        self.chess_type = color
        self.alphabeta_depth = alphabeta_depth
        self.total_nodes = 0

    def alpha_beta_search(self, depth, alpha, beta, our_colour, preMove):
    
        best_move = StoneMove()
        if (is_win_by_premove(self.board, preMove)):
            if (our_colour == self.chess_type):
                #Opponent wins.
                return None, 0
            else:
                #Self wins.
                return None, MININT + 1
        
        if(self.check_first_move()):
            best_move.positions[0].x = 10
            best_move.positions[0].y = 10
            best_move.positions[1].x = 10
            best_move.positions[1].y = 10

            return best_move, alpha
        
        alpha_beta = AlphaBeta()

        tree = TreeNode(
            created_move = None,
            level = 0,
            slelection_method_is_max = 1,
            board = self.board,
            hot_board = self.hot_board,
            color = our_colour,
            total_nodes = 0,
            parent_alpha_beta = alpha_beta
            )
        
        best_move, nodes = tree.expand_tree()
        # best_move = self.find_possible_move()
        return best_move, nodes
        
    def check_first_move(self):
        for i in range(1,len(self.board)-1):
            for j in range(1, len(self.board[i]) - 1):
                if(self.board[i][j] != NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        move = StoneMove()
        found = 0
        for i in range(1,len(self.board)-1):
            for j in range(1, len(self.board[i]) - 1):
                if(self.board[i][j] == NOSTONE):
                    move.positions[found].x = i
                    move.positions[found].y = j
                    found += 1
                    if found == 2:
                        return move
        return move

def flush_output():
    import sys
    sys.stdout.flush()
