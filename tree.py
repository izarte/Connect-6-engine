from defines import *
from calculation_module import evaluate_board
from hot_board import calculate_combination_value
from tools import make_move, unmake_move, is_win_by_premove, my_print, print_board

import itertools
import time


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
        possible_combinations = list(itertools.combinations(self.bdata.hot_board, 2))
        # Check if actual node is a leaf
        if self.is_leaf:
            # self.possible_moves[CalculationModule.calculate()] = None
            self.possible_moves[evaluate_board(self.board, self.my_color, self.weights)] = None
            sorted_combinations = [] # Don't execute loop 
        else:
            t = time.perf_counter()
            maximum = [0]
            sorted_combinations = sorted(
                possible_combinations,
                key=lambda combination: calculate_combination_value(self.board, combination, self.color, maximum),
                reverse=True)
            sorted_combinations = list(itertools.takewhile(lambda x: calculate_combination_value(self.board, x, self.color, maximum) > maximum[0] // 2, sorted_combinations))

        if self.level == 1 and not self.slelection_method_is_max:
            print("FIRST: ", sorted_combinations[0], calculate_combination_value(self.board, sorted_combinations[0], self.color, maximum))

        for combination in sorted_combinations:
            if combination == ((8, 9), (13, 9)) or combination == ((13, 9), (8, 9)):
                print("THIS", calculate_combination_value(self.board, combination, self.color,maximum), "c: ", self.color, self.my_color)
            if self.alpha_beta:
                break
            self.total_nodes += 1
            move = StoneMove(combination)
            # Make move to change actual state
            if is_win_by_premove(self.board, move):
                break
            make_move(self.board, self.bdata, move, BLACK, self.level != DEPTH - 1, False)

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
            for p in self.possible_moves:
                print(p, self.possible_moves[p])
            print(self.slelection_method_is_max, best_option, self.possible_moves[best_option])
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
        # print(self.level)
        if self.is_leaf:
            t = time.perf_counter()
            v = evaluate_board(self.board, self.my_color, self.weights)
            # my_print(f"EVALUTAION {time.perf_counter() - t}", "puta.txt")
            return v, self.total_nodes

        t = time.perf_counter()
        possible_combinations = list(itertools.combinations(self.hot_board, 2))
        maximum = [0]
        sorted_combinations = sorted(
            possible_combinations,
            key=lambda combination: calculate_combination_value(self.board, self.hot_board, combination, self.color, maximum),
            reverse=True)
        # my_print(f"COMBINATION {time.perf_counter() - t}", "puta.txt")
        # print(len(sorted_combinations))
        sorted_combinations = list(itertools.takewhile(lambda x: calculate_combination_value(self.board, self.hot_board, x, self.color, 0) > maximum // 2, sorted_combinations))
        # print(len(sorted_combinations))
        # sorted_combinations = sorted_combinations[:100]
        a = self.alpha_beta.alpha
        b = self.alpha_beta.beta
        best_move = StoneMove()
        for i, combination in enumerate(sorted_combinations):
            # my_print(f"{self.level} {combination}", "puta.txt")
            self.total_nodes += 1
            move = StoneMove(combination)
            make_move(board=self.board, hot_board=self.hot_board, remembered_moves=self.remembered_moves, move=move, color=self.color, store=self.level != DEPTH - 1)
            
            alpha_beta = AlphaBeta(alpha=-b, beta=-a)
            node = TreeNode(
                created_move=move,
                level=(self.level + 1),
                slelection_method_is_max = not self.slelection_method_is_max,
                board=self.board,
                hot_board=self.hot_board,
                remembered_moves=self.remembered_moves,
                color=self.color ^ 3,
                my_color=self.my_color,
                total_nodes=self.total_nodes,
                parent_alpha_beta=alpha_beta
            )

            score, self.total_nodes = node.negaScout()
            score = -score
            if a < score and score < self.alpha_beta.beta and i > 0 and not self.is_leaf:
                node.alpha_beta = AlphaBeta(alpha=-self.alpha_beta.beta, beta=-score)
                a, self.total_nodes = node.negaScout()
                a = -a
            unmake_move(board=self.board, hot_board=self.hot_board, remembered_moves=self.remembered_moves, move=move)
            a = max(a, score)
            if a == score:
                best_move = move
            if a >= self.alpha_beta.beta:
                break
            b = a + 1

        if self.level == 0:
            return best_move, a, self.total_nodes
        return a, self.total_nodes
