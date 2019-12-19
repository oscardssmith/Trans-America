#!/usr/bin/python3
""" ta.py
    Run the Trans America AI competition

    This file is the mainline for starting single games and tournaments.
"""
import copy
import argparse
import re
from game import Game
import window
import simple

def run_tournament(args):
    """  Run num games against several ais, printing who wins """
    if len(args.players) != 2:
        print("Error: we only run 2 player tournaments right now.")
        exit(1)

    ai1 = lookup_ai(args.players[0])
    ai2 = lookup_ai(args.players[1])
    wins = [0, 0, 0]
    while sum(wins) < args.tournament:
        players = [[0, ai1], [1, ai2]]
        game = Game(players)

        board = copy.deepcopy(game.board)
        hands = copy.deepcopy(game.hands)
        winner1 = game.play_game()

        game2 = Game([[0, ai2], [1, ai1]], board, hands)
        winner2 = game2.play_game()
        if winner1 != winner2:
            print(winner1)
            wins[winner1] += 1
        else:
            print("draw")
            wins[2] += 1
    print(wins)

def lookup_ai(name):
    """ Return which AI to use based on a name """
    if name == "simple":
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

def run_one(args):
    """  Run a game and optionally display it graphically """
    players = []
    for i in range(0, len(args.players)):
        players.append([i, lookup_ai(args.players[i])])
    game = Game(players)

    if args.view:
        width, height = lookup_geometry(args)
        win = window.Window(width, height, args.scaled)
    else:
        win = None

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

    if args.tournament:
        run_tournament(args)
    else:
        run_one(args)

if __name__ == '__main__':
    main()
