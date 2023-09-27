from tools import *

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

    def alpha_beta_search(self, depth, alpha, beta, ourColor, preMove):
    
        #Check game result
        best_move = StoneMove()
        if (is_win_by_premove(self.m_board, preMove)):
            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0
            else:
                #Self wins.
                return MININT + 1
        
        alpha = 0
        if(self.check_first_move()):
            best_move.positions[0].x = 10
            best_move.positions[0].y = 10
            best_move.positions[1].x = 10
            best_move.positions[1].y = 10
        else:   
            move1 = self.find_possible_move()
            best_move.positions[0].x = move1[0]
            best_move.positions[0].y = move1[1]
            best_move.positions[1].x = move1[0]
            best_move.positions[1].y = move1[1]
            make_move(self.m_board,best_move,ourColor)
            
            '''#Check game result
            if (is_win_by_premove(self.m_board, best_move)):
                #Self wins.
                return MININT + 1;'''
            
            move2 = self.find_possible_move()
            best_move.positions[1].x = move2[0]
            best_move.positions[1].y = move2[1]
            make_move(self.m_board,best_move,ourColor)

        return best_move, alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i]) - 1):
                if(self.m_board[i][j] != NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i]) - 1):
                if(self.m_board[i][j] == NOSTONE):
                    return (i,j)
        return (-1,-1)

def flush_output():
    import sys
    sys.stdout.flush()
