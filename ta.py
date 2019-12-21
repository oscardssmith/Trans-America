#!/usr/bin/python3
""" ta.py
    Run the Trans America AI competition

    This file is the mainline for starting single games and tournaments.
"""
import copy
import argparse
import re
from itertools import permutations
import importlib
from game import Game
import window
import util

def run_tournament(args, win):
    """  Run num games against several ais, printing who wins """
    matches = list(permutations(range(0, len(args.players))))
    scores = []
    wins = []
    for _ in range(0, len(args.players)):
        scores.append(0)
        wins.append(0)

    for _ in range(0, args.tournament):
        board = None
        hands = None
        for match in matches:
            players = []
            for i, player in enumerate(match):
                players.append(lookup_ai(args.players[player]))

            game = Game(players, board, hands)
            if board is None:
                board = copy.deepcopy(game.board)
            if hands is None:
                hands = copy.deepcopy(game.hands)

            game.play_game()
            standings = game.board.get_totals(game.hands)
            for i, player in enumerate(match):
                scores[player] += standings[i]
                if standings[i] == 0:
                    wins[player] += 1

            if win:
                win.draw(game.board, game.hands)
                win.draw_standings(standings)
                if not util.wait_for_key():
                    break
                win.clear()

    print("Scores: {}".format(scores))
    print("Wins:   {}".format(wins))


def lookup_ai(name):
    """ Return which AI to use based on a name """
    try:
        module = importlib.import_module(name)
    except ImportError:
        print("Error: {} is not a valid AI.".format(name))
        exit(1)

    return module.create()

def lookup_geometry(args):
    """ Parse a --geometry stanza """
    width = 1600
    height = 900
    if args.geometry:
        findx = re.search("^([0-9]*)[xX]([0-9]*)$", args.geometry)
        if findx is None:
            print("Invalid geometry.  Specify WIDTHxHEIGHT.")
            exit(1)
        width = int(findx.group(1))
        height = int(findx.group(2))

    return width, height

def run_one(args, win):
    """  Run a game and optionally display it graphically """
    players = []
    for i in range(0, len(args.players)):
        players.append(lookup_ai(args.players[i]))
    game = Game(players)

    game.play_game(win, args.wait)

def main():
    """ Run the main program """
    parser = argparse.ArgumentParser(description='Run a Trans America simulation.')
    parser.add_argument('--geometry', dest='geometry', metavar='WxH', default='1600x900',
                        help='Specify width and height to display (i.e. 1024x768)')
    parser.add_argument('players', action='store', nargs='*', metavar='player',
                        help='Specify the name of one or more AI to run as a player',
                        default='simple')
    parser.add_argument('--view', action='store_true', dest='view', default=False,
                        help='If specified, you can watch the game play out.')
    parser.add_argument('--scaled', action='store_true', dest='scaled', default=False,
                        help='If specified, scale the map to be human comfortable.')
    parser.add_argument('--wait', action='store_true', dest='wait', default=False,
                        help='Wait for the user to press the "w" key for each turn to proceed.')
    parser.add_argument('--tournament', dest='tournament', metavar='rounds', type=int,
                        help='Play a tournament of the given number of rounds.')

    args = parser.parse_args()

    win = None
    if args.view:
        width, height = lookup_geometry(args)
        win = window.Window(width, height, args.scaled)

    if args.tournament:
        run_tournament(args, win)
    else:
        run_one(args, win)

if __name__ == '__main__':
    main()
