import itertools
import time
import copy
import numpy as np

from defines import *
from calculation_module import evaluate_board
from hot_board import calculate_combination_value
from tools import make_move, unmake_move, is_win, future_score
from hot_board import update_hot_board


# Define a function to calculate combination values in parallel
def calculate_combination_value_parallel(combination, board, color, maximum):
    return calculate_combination_value(board, combination, color, maximum, True)


class TreeNode:
    def __init__(self, created_move, level, slelection_method_is_max, board, bdata, color, my_color, total_nodes, parent_alpha_beta, weights=None):
        self.created_move = created_move
        self.slelection_method_is_max = slelection_method_is_max
        self.board = board
        self.bdata = bdata
        self.color = color
        self.my_color = my_color
        # Dictonary with labels as score and keys as move that creates scored scenario
        self.possible_moves = {}
        self.level = level
        self.is_leaf = True if self.level == DEPTH else False
        self.total_nodes = total_nodes
        self.parent_alpha_beta = parent_alpha_beta
        self.alpha_beta = AlphaBeta(parent_alpha_beta.alpha, parent_alpha_beta.beta)
        self.weights = weights


    """
        Calculates all possible moves and expand tree for each posibility until depth is reached
    """
    def expand_tree(self, last_level = 0):
        # Check if actual node is a leaf
        if self.is_leaf:
            self.possible_moves[evaluate_board(self.board, self.my_color, self.created_move, self.weights)] = None
            sorted_combinations = [] # Don't execute loop 
        else:
            update_hot_board(self.board, self.bdata)
            # t = time.perf_counter()
            possible_combinations = list(itertools.combinations(self.bdata.hot_board, 2))
            maximum = [0]
            # t1 = time.perf_counter()
            sorted_combinations = sorted(
                possible_combinations,
                key=lambda combination: calculate_combination_value(self.board, combination, self.color, maximum),
                reverse=True)
            # t2 = time.perf_counter()
            sorted_combinations  = list(itertools.takewhile(lambda x: calculate_combination_value(self.board, x, self.color) > maximum[0] // 2, sorted_combinations))
            sorted_combinations = sorted_combinations[:20]
            # print(f"COMBINATION: {t1 - t} SORTING: {t2 - t1} FILTER {time.perf_counter() - t2}")

            # print(len(sorted_combinations))

        for combination in sorted_combinations:
            if self.alpha_beta:
                break
            self.total_nodes += 1
            move = StoneMove(combination)
            expand = True
            # Make move to change actual state
            make_move(self.board, self.bdata, move, self.color, self.level != DEPTH - 1, False)
            if is_win(self.board, move, self.color):
                score = evaluate_board(self.board, self.my_color, move, self.weights)
                expand = False
                unmake_move(self.board, self.bdata, move)

            if expand:
                # Create child
                node = TreeNode(
                    created_move = move,
                    level = (self.level + 1),
                    slelection_method_is_max = not self.slelection_method_is_max,
                    board = self.board,
                    bdata = self.bdata,
                    color = self.color ^ 3,
                    my_color = self.my_color,
                    total_nodes = self.total_nodes,
                    parent_alpha_beta = self.alpha_beta,
                    weights=self.weights
                )

                score, self.total_nodes = node.expand_tree(last_level)
                # Unmake move to return original state (at this point all childs have been explored)
                unmake_move(self.board, self.bdata, move)

            self.possible_moves[score] = None
            if self.level == 0:
                self.possible_moves[score] = move

            if self.slelection_method_is_max:
            # If is max turn
                if score < self.alpha_beta.alpha:
                    if score == abs(MAXINT):
                        break
                    continue
                self.alpha_beta.alpha = score
            else:
            # If is min turn
                if score > self.alpha_beta.beta:
                    if score == abs(MAXINT):
                        break
                    continue
                self.alpha_beta.beta = score
            if score == abs(MAXINT):
                break
            
        best_option = self.get_selection()
        # Return the best move if it is first node
        if self.level == 0:
            return self.possible_moves[best_option], best_option, self.total_nodes
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
            return last value in ordered possible_moves as it will be maximun
        When selection method_is_max is min turn (False):
            return first value in ordered possible_moves as it will be minimum
    """
    def get_selection(self):
        if self.slelection_method_is_max:
            return max(self.possible_moves) if self.possible_moves else MAXINT
        return min(self.possible_moves) if self.possible_moves else MININT      

    def negaScout(self):
        if self.is_leaf:
            # t = time.perf_counter()
            v = evaluate_board(self.board, self.my_color, self.created_move, self.weights)
            # my_print(f"EVALUTAION {time.perf_counter() - t}", "puta.txt")
            return v, self.total_nodes

        t = time.perf_counter()
        possible_combinations = list(itertools.combinations(self.bdata.hot_board, 2))
        maximum = [0]
        # t1 = time.perf_counter()
        sorted_combinations = sorted(
            possible_combinations,
            key=lambda combination: calculate_combination_value(self.board, combination, self.color, maximum),
            reverse=True)
        # t2 = time.perf_counter()
        sorted_combinations  = list(itertools.takewhile(lambda x: calculate_combination_value(self.board, x, self.color) > maximum[0] // 2, sorted_combinations))
        sorted_combinations = sorted_combinations[:20]
        # my_print(f"COMBINATION {time.perf_counter() - t}", "puta.txt")
        # print(len(sorted_combinations))
        # sorted_combinations = list(itertools.takewhile(lambda x: calculate_combination_value(self.board, self.hot_board, x, self.color, 0) > maximum // 2, sorted_combinations))
        # print(len(sorted_combinations))
        # sorted_combinations = sorted_combinations[:100]
        a = self.alpha_beta.alpha
        b = self.alpha_beta.beta
        best_move = StoneMove()
        for i, combination in enumerate(sorted_combinations):
            # my_print(f"{self.level} {combination}", "puta.txt")
            self.total_nodes += 1
            move = StoneMove(combination)
            make_move(self.board, self.bdata, move, self.color, self.level != DEPTH - 1, False)

            
            alpha_beta = AlphaBeta(alpha=-b, beta=-a)
            node = TreeNode(
                created_move = move,
                level = (self.level + 1),
                slelection_method_is_max = not self.slelection_method_is_max,
                board = self.board,
                bdata = self.bdata,
                color = self.color ^ 3,
                my_color = self.my_color,
                total_nodes = self.total_nodes,
                parent_alpha_beta = alpha_beta,
                weights=self.weights
            )

            score, self.total_nodes = node.negaScout()
            score = -score
            if a < score and score < self.alpha_beta.beta and i > 0 and not self.is_leaf:
                node.alpha_beta = AlphaBeta(alpha=-self.alpha_beta.beta, beta=-score)
                a, self.total_nodes = node.negaScout()
                a = -a
            unmake_move(self.board, self.bdata, move)

            a = max(a, score)
            if a == score:
                best_move = move
            if a >= self.alpha_beta.beta:
                break
            b = a + 1

        if self.level == 0:
            return best_move, a, self.total_nodes
        return a, self.total_nodes
