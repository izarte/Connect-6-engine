from defines import *
from calculation_module import CalculationModule
from tools import make_move, unmake_move

import itertools


class TreeNode:
    def __init__(self, created_move, level, slelection_method_is_max, board, hot_board, color, total_nodes):
        self.created_move = created_move
        self.slelection_method_is_max = slelection_method_is_max
        self.board = board
        self.hot_board = hot_board
        self.color = color
        # Dictonary with labels as score and keys as move that creates scored scenario
        self.posible_moves = {}
        self.level = level
        self.is_leaf = True if self.level == DEPTH else False
        self.total_nodes = total_nodes


    def expand_tree(self):
        posible_combinations = list(itertools.combinations(self.hot_board, 2))
        # Next children are leafs if next depth level is DEPTH
        for combination in posible_combinations:
            self.total_nodes += 1
            if self.is_leaf:
                self.posible_moves[CalculationModule.calculate()] = None
                continue
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
                total_nodes = self.total_nodes
            )
            score, self.total_nodes = node.expand_tree()
            # Only save movements for first node
            self.posible_moves[score] = None
            if self.level == 0:
                self.posible_moves[score] = move
            # Unmake move to return original state (at this point all childs have been explored)
            unmake_move(self.board, self.hot_board, move)
        best_option = self.get_selection()
        # Return the best move if it is first node
        if self.level == 0:
            return self.posible_moves[best_option], self.total_nodes
        # Return the best value if it is a leaf or an intermediate level
        return best_option, self.total_nodes

    """
        Return best value due to max or min selection method
        When slection method is max (True):
            return last value in ordered posible_moves as it will be maximun
        When selection methos is min (False):
            return first value in ordered posible_moves as it will be minimum
    """
    def get_selection(self):
        if self.slelection_method_is_max:
            return sorted(self.posible_moves)[-1]
        return sorted(self.posible_moves)[0]
