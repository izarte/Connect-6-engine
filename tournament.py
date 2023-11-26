import random
import time

from defines import *
from tools import init_board, make_move, check_full, is_win

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

    def dummy(self):
        for match in self.matches:
            self.scores[match[WHITE]] += 1

    def play_matches(self, search_function):
        for match in self.matches:
            t = time.perf_counter()
            board = init_board()
            bdata = {
                BLACK: BData(),
                WHITE: BData() 
            }
            move = StoneMove()
            color = BLACK
            tournament_data = {
                BLACK: {'color': color, 'board' : board, 'bdata': bdata, 'weights': []},
                WHITE: {'color': color, 'board' : board, 'bdata': bdata, 'weights': []}
            }
            print("Match between")
            print(f"White: {match[WHITE]} {self.participants[match[WHITE]]}")
            print(f"Black: {match[BLACK]} {self.participants[match[BLACK]]}")
            while not check_full(board) and not is_win(board, move, color):
                color = color ^ 3
                tournament_data[color]['color'] = color
                tournament_data[color]['board'] = board
                tournament_data[color]['bdata'] = bdata[color]
                tournament_data[color]['weights'] = self.participants[match[color]]
                move = search_function(color, move, self.participants[match[color]], tournament_data=tournament_data[color])
                make_move(board, bdata[color], move, color)
                make_move(board, bdata[color ^ 3], move, color)

            winner = color
            self.scores[match[winner]] += 1
            if winner == WHITE:
                print(f"WHITE won id: {match[winner]} score: {self.scores[match[winner]]}")
            else:
                print(f"BLACK won id: {match[winner]} score: {self.scores[match[winner]]}")
            print("TIME:", time.perf_counter() - t)
        
