import random
import copy

from defines import *
from tools import is_win_by_premove, make_move, check_full, print_board

class Tournament():
    def __init__(self, participants):
        self.participants = participants
        self.matches = []
        self.scores = [0 for _ in self.participants]

    def create_matches(self, score_requisite):
        random.shuffle(self.participants)
        self.matches = []
        player_1 = None

        for i, score in enumerate(self.scores):
            if score == score_requisite:
                if player_1 == None:
                    player_1 = i
                else:
                    match = {WHITE: player_1, BLACK: i}
                    self.matches.append(match)
                    player_1 = None

    def play_matches(self, p_board, p_hot_board, search_function):
        for match in self.matches:
            board = copy.deepcopy(p_board)
            hot_board = copy.deepcopy(p_hot_board)
            move = StoneMove()
            color = BLACK
            tournament_data = {'color': color, 'board' : board, 'hot_board': hot_board}
            print(f"Match between {match[WHITE]} and {match[BLACK]}")
            while not check_full(board) and not is_win_by_premove(board, move):
                color = color ^ 3
                tournament_data['color'] = color
                tournament_data['board'] = board
                tournament_data['hot_board'] = hot_board
                move = search_function(color, move,self.participants[match[color]], tournament_data=tournament_data)
                make_move(board, hot_board, move, color)
                # print_board(board)
                # input()
            winner = color
            self.scores[match[winner]] += 1
            if winner == WHITE:
                print(f"WHITE won id: {match[winner]} score: {self.scores[match[winner]]}")
            else:
                print(f"BLACK won id: {match[winner]} score: {self.scores[match[winner]]}")
