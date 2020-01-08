""" Template AI.  Useful as a base class """
import sys

def create():
    """ Return an AI """
    return Template()

class Template:
    """ A sub class for AIs """

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
        return 0

    def place_hub(self, board, state): # pylint: disable=W0613,R0201
        """ Return where we want our hub """
        print("Error: you cannot actually use the template AI")
        sys.exit(1)

    def move(self, board, tracks_left, state): # pylint: disable=W0613,R0201
        """ Figure out our move """
        print("Error: you cannot actually use the template AI")
        sys.exit(1)

    def see_hub(self, num, move):
        """ Receive a hub placement made by a player """

    def see_move(self, num, move):
        """ Receive a move made by a player """
