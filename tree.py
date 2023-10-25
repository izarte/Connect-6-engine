from defines import *
from calculation_module import CalculationModule, evaluate_board
from tools import make_move, unmake_move, my_print

import itertools


class TreeNode:
    def __init__(self, created_move, level, slelection_method_is_max, board, hot_board, color, my_color, total_nodes, parent_alpha_beta):
        self.created_move = created_move
        self.slelection_method_is_max = slelection_method_is_max
        self.board = board
        self.hot_board = hot_board
        self.color = color
        self.my_color = my_color
        # Dictonary with labels as score and keys as move that creates scored scenario
        self.posible_moves = {}
        self.level = level
        self.is_leaf = True if self.level == DEPTH else False
        self.total_nodes = total_nodes
        self.parent_alpha_beta = parent_alpha_beta
        self.alpha_beta = AlphaBeta(parent_alpha_beta.alpha, parent_alpha_beta.beta)


    """
        Calculates all possible moves and expand tree for each posibility until depth is reached
    """
    def expand_tree(self, last_level = 0):
        posible_combinations = list(itertools.combinations(self.hot_board, 2))
        # Check if actual node is a leaf
        if self.is_leaf:
            self.posible_moves[CalculationModule.calculate()] = None
            # self.posible_moves[evaluate_board(self.board, self.my_color)] = None
            posible_combinations = [] # Don't execute loop

        for combination in posible_combinations:
            # Check min-max condition to stop expanding
            if self.alpha_beta:
                break
            self.total_nodes += 1
            move = StoneMove(combination)
            # Make move to change actual state
            make_move(self.board, self.hot_board, move, self.color)
            # Create child
            node = TreeNode(
                created_move = move,
                level = (self.level + 1),
                slelection_method_is_max = not self.slelection_method_is_max,
                board = self.board,
                hot_board = self.hot_board,
                color = self.color ^ 3,
                my_color = self.my_color,
                total_nodes = self.total_nodes,
                parent_alpha_beta = self.alpha_beta
            )

            score, self.total_nodes = node.expand_tree(last_level)
            # Unmake move to return original state (at this point all childs have been explored)
            unmake_move(self.board, self.hot_board, move)
            # Only save movements for first node
            self.posible_moves[score] = None
            if self.level == 0:
                self.posible_moves[score] = move
            
            # If is max turn
                if score < self.alpha_beta.alpha:
                    continue
                self.alpha_beta.alpha = score
            else:
            # If is min turn
                if score > self.alpha_beta.beta:
                    continue
                self.alpha_beta.beta = score
            
        best_option = self.get_selection()
        # Return the best move if it is first node
        if self.level == 0:
            return self.posible_moves[best_option], best_option, self.total_nodes
        # Update parent alpha beta values
        if self.slelection_method_is_max:
            if best_option < self.parent_alpha_beta.beta:
                self.parent_alpha_beta.beta = best_option
        else:
            if best_option > self.parent_alpha_beta.alpha:
                self.parent_alpha_beta.alpha = best_option

        # Return the best value if it is a leaf or an intermediate level
        return best_option, self.total_nodes


    """
        Return best value due to max or min selection method
        When slection_method_is_max is max turn (True):
            return last value in ordered posible_moves as it will be maximun
        When selection method_is_max is min turn (False):
            return first value in ordered posible_moves as it will be minimum
    """
    def get_selection(self):
        if self.slelection_method_is_max:
            return max(self.posible_moves)
        return min(self.posible_moves)
