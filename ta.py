#!/usr/bin/python3
""" ta.py
    Run the Trans America AI competition

    This file is the mainline for starting single games and tournaments.
"""
import copy
import argparse
import re
from itertools import permutations
from game import Game
import window
import util
import simple

def run_tournament(args, win):
    """  Run num games against several ais, printing who wins """
    matches = list(permutations(range(0, len(args.players))))

    for _ in range(0, args.tournament):
        board = None
        hands = None
        for match in matches:
            players = []
            for player in match:
                players.append([player, lookup_ai(args.players[player])])

            game = Game(players, board, hands)
            if board is None:
                board = copy.deepcopy(game.board)
            if hands is None:
                hands = copy.deepcopy(game.hands)

            ret = game.play_game()

            if win:
                win.draw(game.board, game.hands)
                if not util.wait_for_key():
                    break

            print(ret)

def lookup_ai(name):
    """ Return which AI to use based on a name """
    if name == simple.Simple.name():
        return simple
    return False

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
        players.append([i, lookup_ai(args.players[i])])
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

    for player in args.players:
        if not lookup_ai(player):
            print("Error: {} is not a valid AI name.".format(player))
            exit(1)

    if args.view:
        width, height = lookup_geometry(args)
        win = window.Window(width, height, args.scaled)

    if args.tournament:
        run_tournament(args, win)
    else:
        run_one(args, win)

if __name__ == '__main__':
    main()
