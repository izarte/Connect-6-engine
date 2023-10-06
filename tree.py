from defines import *
from calculation_module import CalculationModule
from tools import make_move

import itertools
import copy


class TreeNode:
    def __init__(self, created_move, level, selection_method, board, hot_board, color, total_nodes):
        self.created_move = created_move
        self.slelection_method_is_max = selection_method
        self.board = board
        self.hot_board = hot_board
        self.color = color
        # Dictonary with labels as score and keys as move that creates scored scenario
        self.posible_moves = {}
        self.is_leaf = True if level == DEPTH else False
        self.total_nodes = total_nodes


    def expand_tree(self):
        posible_combinations = list(itertools.combinations(self.hot_board, 2))
        # Next children are leafs if next depth level is DEPTH
        for combination in posible_combinations:
            if self.is_leaf:
                self.posible_moves[CalculationModule.calculate()] = None
                continue
            move = StoneMove(combination)
            # Create copies of boards to make sure parent board isn't changed during expansion
            current_board = copy.deepcopy(self.board)
            current_hot_board = copy.deepcopy(self.hot_board)
            make_move(current_board, current_hot_board, move, self.color)
            # Create child
            node = TreeNode(
                created_move = move,
                level = (self.level + 1),
                selection_method = not self.selection_method,
                board = current_board,
                hot_board = current_hot_board,
                color = self.color ^ 3
            )
            score, total_nodes = node.expand_tree()
            self.total_nodes += total_nodes
            # Only save movements for first node
            self.posible_moves[score] = None
            if self.level == 0:
                self.posible_moves[score] = self.move
        best_option = self.get_selection()
        # Return the best move if it is first node
        if self.level == 0:
            return self.posible_moves[best_option], len(self.posible_moves) +
        # Return the best value if it is a leaf or an intermediate level
        return best_option

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
