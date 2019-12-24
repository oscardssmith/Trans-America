""" Stupid AI.  Just place track randomly """
import random
from state import ALL

def create():
    """ Return an AI """
    return Guess()

class Guess:
    """ A class to hold the stupidest AI algorithm """

    def __init__(self):
        self.num = None
        self.player_count = 0
        self.hub = None
        self.hand = None
        self.board = None

    def start(self, num, player_count, board, hand):
        """ Construct a random AI """
        self.num = num
        self.player_count = player_count
        self.hand = hand
        self.board = board
        self.hub = None
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

    def move(self, board, tracks_left, state): # pylint: disable=W0613
        """ Figure out our move """
        #After, look at all the possible moves,  and pick one
        possible_moves = list(state.legal_moves(self.num, 1, tracks_left))
        move = random.randint(0, len(possible_moves) - 1)
        return possible_moves[move]

    def see_move(self, num, move):
        """ Receive a move made by a player """
