from tools import *

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def update_parameters(self, board, color, alphabeta_depth):
        self.m_board = board
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

    def alpha_beta_search(self, depth, alpha, beta, our_colour, preMove):
    
        best_move = StoneMove()
        if (is_win_by_premove(self.m_board, preMove)):
            if (our_colour == self.m_chess_type):
                #Opponent wins.
                return None, 0
            else:
                #Self wins.
                return None, MININT + 1
        
        alpha = MININT
        if(self.check_first_move()):
            best_move.positions[0].x = 10
            best_move.positions[0].y = 10
            best_move.positions[1].x = 10
            best_move.positions[1].y = 10

            return best_move, alpha
         
        best_move = self.find_possible_move()

        return best_move, alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i]) - 1):
                if(self.m_board[i][j] != NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        move = StoneMove()
        found = 0
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i]) - 1):
                if(self.m_board[i][j] == NOSTONE):
                    move.positions[found].x = i
                    move.positions[found].y = j
                    found += 1
                    if found == 2:
                        return move
        return move

def flush_output():
    import sys
    sys.stdout.flush()
