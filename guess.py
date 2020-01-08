""" Stupid AI.  Just place track randomly """
import random
from template import Template
from state import SELECT, ALL

def create():
    """ Return an AI """
    return Guess()

class Guess(Template):
    """ A class to hold the stupidest AI algorithm """

    def start(self, num, player_count, board, hand):
        """ Construct a random AI """
        super().start(num, player_count, board, hand)
        return ALL

    def place_hub(self, board, state): # pylint: disable=W0613
        """ Return where we want out hub """
        while self.hub is None:
            row = random.randint(1, board.rows - 1)
            col = random.randint(1, board.cols - 1)
            self.hub = (row, col)
            for ocean in board.oceans:
                if row == ocean[0] and col == ocean[1]:
                    self.hub = None

            if self.hub is not None:
                return self.hub

    def move(self, board, tracks_left, state):
        """ Figure out our move """
        if state.desired_states & SELECT:
            possible_moves = list(state.fast_get_moves(self.hub, tracks_left))
        else:
            possible_moves = list(state.legal_moves(self.num, 1, tracks_left))
        move = random.randint(0, len(possible_moves) - 1)
        return possible_moves[move]
