from tools import *
from tree import TreeNode


class SearchEngine():
    def __init__(self):
        self.board = None
        self.chess_type = None
        self.alphabeta_depth = None
        self.total_nodes = 0


    def update_parameters(self, board ,bdata, color, alphabeta_depth,):
        self.board = board
        self.bdata = bdata
        self.chess_type = color
        self.alphabeta_depth = alphabeta_depth
        self.total_nodes = 0


    def alpha_beta_search(self, our_colour, preMove, weights):
    
        best_move = StoneMove()
        # if (is_win(self.board, preMove, self.chess_type)):
        #     if (our_colour == self.chess_type):
        #         #Opponent wins.
        #         return None, 0
        #     else:
        #         #Self wins.
        #         return None, MININT + 1
        
        if(self.check_first_move()):
            best_move.positions[0].x = 10
            best_move.positions[0].y = 10
            best_move.positions[1].x = 10
            best_move.positions[1].y = 10

            return best_move, MAXINT, 1
        
        # Create alpha beta object
        alpha_beta = AlphaBeta()
        # Create first node to expand
        tree = TreeNode(
            created_move = None,
            level = 0,
            slelection_method_is_max = True,
            board = self.board,
            bdata = self.bdata,
            color = our_colour,
            my_color = our_colour,
            total_nodes = 0,
            parent_alpha_beta = alpha_beta,
            weights = weights
            )
        
        best_move, score, nodes = tree.expand_tree()
        return best_move, score, nodes


    def negascout_search(self, our_colour, preMove, weights):
    
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

            return best_move, MAXINT, 1
        
        alpha_beta = AlphaBeta()

        tree = TreeNode(
            created_move = None,
            level = 0,
            slelection_method_is_max = True,
            board = self.board,
            bdata = self.bdata,
            color = our_colour,
            my_color = our_colour,
            total_nodes = 0,
            parent_alpha_beta = alpha_beta,
            weights = weights
            )
        
        best_move, score, nodes = tree.negaScout()
        # best_move = self.find_possible_move()
        return best_move, score, nodes


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
