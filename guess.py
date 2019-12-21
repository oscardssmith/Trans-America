""" Stupid AI.  Just place track randomly """
import random
import features

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

    def start(self, num, player_count, hand):
        """ Construct a random AI """
        self.num = num
        self.player_count = player_count
        self.hand = hand
        self.hub = None


    def place_hub(self, board_state):
        """ Return where we want out hub """
        while self.hub is None:
            row = random.randint(1, features.LAST_ROW - 1)
            col = random.randint(1, features.LAST_COLUMN - 1)
            self.hub = (row, col)
            for ocean in features.OCEANS:
                if row == ocean[0] and col == ocean[1]:
                    self.hub = None

            if self.hub is not None:
                return self.hub

    def move(self, board_state, tracks_left):
        """ Figure out our move """
        #After, look at all the possible moves,  and pick one
        board_state.tracks_left = tracks_left
        possible_moves = list(board_state.get_moves(self.hub))
        move = random.randint(0, len(possible_moves) - 1)
        return possible_moves[move]

    def see_move(self, num, move, board_state):
        """ Receive a move made by a player """
