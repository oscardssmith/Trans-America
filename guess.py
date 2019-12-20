""" Stupid AI.  Just place track randomly """
#Protip: Don't name your variables board
import random

def init(board, features, name, hands):
    """ Return an AI """
    return Guess(board, features, name, hands)

class Guess:
    """ A class to hold the stupidest AI algorithm """

    def __init__(self, board, features, name, hands):
        """ Construct a random AI """
        self.name = name
        self.features = features
        self.hands = hands
        self.board = board
        self.hub = None


    @staticmethod
    def name():
        """ Return the name of this class """
        return "guess"

    def move(self, board):
        """ Figure out our move """
        #Place the hub first
        while self.hub is None:
            row = random.randint(1, self.board.size()[0] - 1)
            col = random.randint(1, self.board.size()[1] - 1)
            self.hub = (row, col)
            for ocean in self.features.OCEANS:
                if row == ocean[0] and col == ocean[1]:
                    self.hub = None

            if self.hub is not None:
                return self.hub

        #After, look at all the possible moves,  and pick one
        possible_moves = list(board.get_moves(self.hub))
        move = random.randint(0, len(possible_moves) - 1)
        return possible_moves[move]
