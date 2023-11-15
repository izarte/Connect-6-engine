from defines import *
from tools import *
import sys
from search_engine import SearchEngine
import time
import math

from genetic import Genetic
from tournament import Tournament
from calculation_module import evaluate_board


class GameEngine:
    def __init__(self, name=ENGINE_NAME):
        if name and len(name) > 0:
            if len(name) < MSG_LENGTH:
                self.m_engine_name = name
            else:
                print(f"Too long Engine Name: {name}, should be less than: {MSG_LENGTH}")
        self.m_alphabeta_depth = DEPTH
        self.m_board = t = [ [0]*GRID_NUM for i in range(GRID_NUM)]
        self.bdata = BData()
        self.init_game()
        self.m_search_engine = SearchEngine()
        self.m_best_move = StoneMove()
        self.weights = [50, 1, -100, -1]

    def init_game(self):
        init_board(self.m_board)

    def on_help(self):
        print(
            f"On help for GameEngine {self.m_engine_name}\n"
            " name        - print the name of the Game Engine.\n"
            " print       - print the board.\n"
            " exit/quit   - quit the game.\n"
            " black XXXX  - place the black stone on the position XXXX on the board.\n"
            " white XXXX  - place the white stone on the position XXXX on the board, X is from A to S.\n"
            " next        - the engine will search the move for the next step.\n"
            " move XXXX   - tell the engine that the opponent made the move XXXX,\n"
            "              and the engine will search the move for the next step.\n"
            " new black   - start a new game and set the engine to black player.\n"
            " new white   - start a new game and set it to white.\n"
            " depth d     - set the alpha beta search depth, default is 6.\n"
            " vcf         - set vcf search.\n"
            " unvcf       - set none vcf search.\n"
            " help        - print this help.\n"
            " genetic     - start genetic competition.\n"
        )

    def run(self):
        msg = ""
        self.on_help()

        while True:
            msg = input().strip()
            log_to_file(msg)
            if msg == "name":
                print(f"name {self.m_engine_name}")
            elif msg == "exit" or msg == "quit":
                break
            elif msg == "print":
                print_board(self.m_board, self.m_best_move)
            elif msg == "vcf":
                self.m_vcf = True
            elif msg == "unvcf":
                self.m_vcf = False
            elif msg.startswith("black"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.bdata, self.m_best_move, BLACK)
                self.m_chess_type = BLACK
                write_hot_board(self.bdata.hot_board)
            elif msg.startswith("white"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.bdata, self.m_best_move, WHITE)
                write_hot_board(self.bdata.hot_board)
                self.m_chess_type = WHITE
            # THIS IS EXECUTED BY INTERFACE (very true)
            elif msg == "next":
                # XOR operator to change player turn
                self.m_chess_type = self.m_chess_type ^ 3
                self.m_best_move = self.search_a_move(self.m_chess_type, self.m_best_move)
                make_move(self.m_board, self.bdata, self.m_best_move, self.m_chess_type)
                score = evaluate_board(board=self.m_board, my_color=self.m_chess_type, genetic_weights=self.weights, t=True)
                print(f"NODES: {self.m_search_engine.total_nodes} SCORE: {score}")
                msg = f"move {move2msg(self.m_best_move)}"
                print(msg)
                flush_output()
                write_hot_board(self.bdata.hot_board)
            elif msg.startswith("new"):
                self.init_game()
                if msg[4:] == "black":
                    self.m_best_move = msg2move("JJ")
                    make_move(self.m_board, self.bdata, self.m_best_move, BLACK)
                    self.m_chess_type = BLACK
                    msg = "move JJ"
                    print(msg)
                    flush_output()
                else:
                    self.m_chess_type = WHITE
            elif msg.startswith("move"):
                self.m_best_move = msg2move(msg[5:])
                make_move(self.m_board, self.bdata, self.m_best_move, self.m_chess_type ^ 3)
                if is_win_by_premove(self.m_board, self.m_best_move):
                    print("We lost!")
                    continue
                self.m_best_move = self.search_a_move(self.m_chess_type, self.m_best_move)
                msg = f"move {move2msg(self.m_best_move)}"
                make_move(self.m_board, self.bdata, self.m_best_move, self.m_chess_type)
                print(msg)
                flush_output()
            elif msg.startswith("depth"):
                d = int(msg[6:])
                if 0 < d < 10:
                    self.m_alphabeta_depth = d
                print(f"Set the search depth to {self.m_alphabeta_depth}.\n")
            elif msg == "help":
                self.on_help()
            elif msg == "t":
                print("TRUE BOARD: ", self.true_board)
                for move in self.remembered_moves['queue']:
                    print(move, end=' - ')
                print("dis: ", end='')
                for move in self.remembered_moves['discarded_queue']:
                    print(move, end=' - ')
            elif msg == "genetic":
                POPULATION = 8
                EPOCHS = 5
                genetic = Genetic(POPULATION, 5)
                iterations = int(math.log2(POPULATION))  
                print(f"Iterations: {iterations} for {len(genetic.population)} chromosomes")    
                for epoch in range(EPOCHS):
                    # print(genetic.population) 
                    tournament = Tournament(genetic.population)
                    for i in range(iterations):
                        tournament.create_matches(score_requisite=i)
                        tournament.play_matches(self.m_board, self.bdata.hot_board, self.remembered_moves, self.search_a_move)
                        # print(tournament.scores)
                    genetic.set_evaluations(tournament.scores)
                    genetic.reproduction()
                print(genetic.population, genetic.evaluations)
                best_weights = []
                p = 0
                for i, weights in enumerate(genetic.population):
                    if genetic.evaluations[i] > p:
                        p = genetic.evaluations[i]
                        best_weights = weights
                print(best_weights)
                my_print(f"{best_weights}", "puta.txt")
        return 0

    def search_a_move(self, ourColor, bestMove, weights=None, tournament_data=None):
        score = 0  
        start = 0
        end = 0

        if tournament_data:
            self.m_chess_type = tournament_data['color']
            self.m_board = tournament_data['board']
            self.bdata.hot_board = tournament_data['hot_board']
        
        self.m_search_engine.update_parameters(self.m_board, self.bdata, self.m_chess_type, self.m_alphabeta_depth)
        start = time.perf_counter()
        if not weights:
            weights = self.weights
        bestMove, score, self.m_search_engine.total_nodes = self.m_search_engine.alpha_beta_search(ourColor, bestMove, weights)
        # make_move(self.m_board, self.bdata, self.m_best_move, self.m_chess_type)
        score = evaluate_board(board=self.m_board, my_color=self.m_chess_type, genetic_weights=self.weights, t=True)
        # bestMove, score, self.m_search_engine.total_nodes = self.m_search_engine.negascout_search(ourColor, bestMove, weights)
        end = time.perf_counter()
        # print(f"NODES: {self.m_search_engine.total_nodes} SCORE: {score}")
        # my_print(f"Time: {end - start:.3f}\tNodes: {self.m_search_engine.total_nodes}\tScore: {score:.3f}", "TreeData.txt")
        # print(f"AB Time:\t{end - start:.3f}")
        # print(f"Node:\t{self.m_search_engine.total_nodes}\n")
        # print(f"Score:\t{score:.3f}")

        return bestMove


def flush_output():
    sys.stdout.flush()


# Create an instance of GameEngine and run the game
if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
