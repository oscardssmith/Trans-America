""" AI for a human player.  Use clicks to determine placement """
import pygame
import sys
from template import Template
from state import POINTS
import util

def create():
    """ Return an AI """
    return Human()

class Human(Template):
    """ A class for a human player """

    def start(self, num, player_count, board, hand):
        """ Construct our AI """
        super().start(num, player_count, board, hand)
        return POINTS

    def place_hub(self, board, state): # pylint: disable=W0613
        """ Return where we want out hub """
        state.window.draw_prompt("Click to place hub")
        okay = False
        while not okay:
            click = util.wait_for_click()
            (row, col) = state.window.invert_coords(click[0], click[1])
            okay = True
            if row < 0 or row >= board.rows:
                okay = False
            if col < 0 or col >= board.cols:
                okay = False
            for ocean in board.oceans:
                if row == ocean[0] and col == ocean[1]:
                    okay = False
                    break
            if not okay:
                state.window.draw_prompt("Invalid hub location")

        return (row, col)

    def move(self, board, tracks_left, state):
        """ Figure out our move """
        state.window.draw_prompt("Click start and end of track")
        while True:
            click = util.wait_for_click()
            point1 = state.window.invert_coords(click[0], click[1])
            click = util.wait_for_click()
            point2 = state.window.invert_coords(click[0], click[1])
            moves = state.legal_moves(self.num, 1, tracks_left)
            for move in moves:
                if (point1 == move[0] and point2 == move[1] or \
                    point1 == move[1] and point2 == move[0]):
                    return move
            state.window.draw_prompt("Illegal move; try again")

        return(point1, point2)
