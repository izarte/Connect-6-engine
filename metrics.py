import time
from defines import *
from tools import init_board, check_full, make_move, is_win, print_board


def get_metrics(search_function):
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
    i = 0
    weights = [9.25610120440747, 7.8114953554571676, -4.218340326390065, -7.227228346545115, 0.5188678488541704, 3.274194308736795, 1.4250319629338606, -1.9655078736741851]
    data = []
    while not check_full(board) and not is_win(board, move, color) and i < 21:
        print(i)
        color = color ^ 3
        tournament_data[color]['color'] = color
        tournament_data[color]['board'] = board
        tournament_data[color]['bdata'] = bdata[color]
        tournament_data[color]['weights'] = weights
        move, t, nodes, score = search_function(color, move, weights, tournament_data=tournament_data[color], return_metrics=True)
        if score > 200:
            score = 200
        if i != 0:
            data.append([t, nodes, score])
        make_move(board, bdata[color], move, color)
        make_move(board, bdata[color ^ 3], move, color)
        # print_board(board)
        i += 1
    write_csv(data)
    print("Done")

import csv
def write_csv(data):
    with open("experiments/data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerows(data)


import pandas as pd
import matplotlib.pyplot as plt
import os
def plot_graphs():
    folder_path = 'experiments/'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not (os.path.isfile(file_path) and filename.endswith('.csv')):
            continue
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, header=None, names=['times', 'nodes', 'scores'])

        # Plotting the first column
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 3, 1)  # 1 row, 2 columns, plot in position 1
        plt.plot(df['times'], marker='o')
        plt.title('Time per move')
        plt.xlabel('Movement')
        plt.ylabel('Seconds (s)')

        # Plotting the second column
        plt.subplot(1, 3, 2)  # 1 row, 2 columns, plot in position 2
        plt.plot(df['nodes'], marker='o', color='orange')
        plt.title('Explored nodes per move')
        plt.xlabel('Movement')
        plt.ylabel('Nodes')

        # Plotting the second column
        plt.subplot(1, 3, 3)  # 1 row, 2 columns, plot in position 2
        plt.plot(df['scores'], marker='o', color='orange')
        plt.title('Score per move')
        plt.xlabel('Movement')
        plt.ylabel('Score')

        # Adjust layout to prevent overlap of subplots
        plt.tight_layout()

        output_folder = 'experiments/graphs'
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f'{filename[:-4]}.png')
        plt.savefig(output_path)


        # Show the plots
        # plt.show()



if __name__ == '__main__':
    plot_graphs()