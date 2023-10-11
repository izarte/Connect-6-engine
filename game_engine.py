from defines import *
from tools import *
import sys
from search_engine import SearchEngine
import time

class GameEngine:
    def __init__(self, name=ENGINE_NAME):
        if name and len(name) > 0:
            if len(name) < MSG_LENGTH:
                self.m_engine_name = name
            else:
                print(f"Too long Engine Name: {name}, should be less than: {MSG_LENGTH}")
        self.m_alphabeta_depth = 6
        self.m_board = t = [ [0]*GRID_NUM for i in range(GRID_NUM)]
        self.hot_board = {}
        self.init_game()
        self.m_search_engine = SearchEngine()
        self.m_best_move = StoneMove()

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
            " help        - print this help.\n")

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
                make_move(self.m_board, self.hot_board, self.m_best_move, BLACK)
                self.m_chess_type = BLACK
            elif msg.startswith("white"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.hot_board, self.m_best_move, WHITE)
                self.m_chess_type = WHITE
            # THIS IS EXECUTED BY INTERFACE (very true)
            elif msg == "next":
                # XOR operator to change player turn
                self.m_chess_type = self.m_chess_type ^ 3
                self.m_best_move = self.search_a_move(self.m_chess_type, self.m_best_move)
                make_move(self.m_board, self.hot_board, self.m_best_move, self.m_chess_type)
                msg = f"move {move2msg(self.m_best_move)}"
                print(msg)
                flush_output()
            elif msg.startswith("new"):
                self.init_game()
                if msg[4:] == "black":
                    self.m_best_move = msg2move("JJ")
                    make_move(self.m_board, self.hot_board, self.m_best_move, BLACK)
                    self.m_chess_type = BLACK
                    msg = "move JJ"
                    print(msg)
                    flush_output()
                else:
                    self.m_chess_type = WHITE
            elif msg.startswith("move"):
                self.m_best_move = msg2move(msg[5:])
                # make_move(self.m_board, self.hot_board, self.m_best_move, self.m_chess_type ^ 3)
                if is_win_by_premove(self.m_board, self.m_best_move):
                    print("We lost!")
                self.m_best_move = self.search_a_move(self.m_chess_type, self.m_best_move)
                msg = f"move {move2msg(self.m_best_move)}"
                # make_move(self.m_board, self.hot_board, self.m_best_move, self.m_chess_type)
                print(msg)
                flush_output()
            elif msg.startswith("depth"):
                d = int(msg[6:])
                if 0 < d < 10:
                    self.m_alphabeta_depth = d
                print(f"Set the search depth to {self.m_alphabeta_depth}.\n")
            elif msg == "help":
                self.on_help()
        return 0

    def search_a_move(self, ourColor, bestMove):
        score = 0
        start = 0
        end = 0

        start = time.perf_counter()
        
        self.m_search_engine.update_parameters(self.m_board, self.hot_board, self.m_chess_type, self.m_alphabeta_depth)
        bestMove, score = self.m_search_engine.alpha_beta_search(self.m_alphabeta_depth, MININT, MAXINT, ourColor, bestMove)
        end = time.perf_counter()

        print(f"AB Time:\t{end - start:.3f}")
        print(f"Node:\t{self.m_search_engine.total_nodes}\n")
        print(f"Score:\t{score:.3f}")
        return bestMove

def flush_output():
    sys.stdout.flush()


# Create an instance of GameEngine and run the game
if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.run()
