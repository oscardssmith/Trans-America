#!/usr/bin/python3
""" ta.py
    Run the Trans America AI competition

    This file is the mainline for starting single games and tournaments.
"""
import copy
from game import Game
import graphics
import mcts
import minDifferenceAI
import mapFeatures

def run_tournament(num, ai1, ai2):
    """  Run num games against two ais, printing who wins """
    wins = [0, 0, 0]
    while sum(wins) < num:
        players = [[0, ai1], [1, ai2]]
        game = Game(players, mapFeatures)

        board = copy.deepcopy(game.board)
        hands = copy.deepcopy(game.hands)
        winner1 = game.play_game()

        game2 = Game([[0, ai2], [1, ai1]], mapFeatures, board, hands)
        winner2 = game2.play_game()
        if winner1 != winner2:
            print(winner1)
            wins[winner1] += 1
        else:
            print("draw")
            wins[2] += 1
    print(wins)

def run_graphics(ai1, ai2):
    """  Run a game and display it graphically """
    players = [[0, ai1], [1, ai2]]
    game = Game(players, mapFeatures)

    window = graphics.window(graphics.xres, graphics.yres, mapFeatures)

    game.play_game(window, True)
    print(game.board.value(game.hands))

if __name__ == '__main__':
    run_graphics(mcts, minDifferenceAI)
    #run_graphics(minTotalAI, minDifferenceAI)
    #run_tournament(100, mcts, minDifferenceAI)
