""" game.py contains Game control logic for Trans-America """
import random
import copy
import board
import util
import features

class Game:
    ''' class for running a single game. '''

    def __init__(self, players, inboard=None, hands=None):
        self.hands = {}
        self.board = None
        self.players = players
        for player in self.players:
            self.hands[player[0]] = {}
        if inboard is None:
            self.board = board.Board(len(players))
        else:
            self.board = inboard
        if hands is None:
            for key, citygroup in features.CITIES.items():
                values = []
                for i in iter(citygroup.keys()):
                    values.append(i)
                cities = random.sample(values, len(self.players))
                for i in range(0, len(self.players)):
                    self.hands[players[i][0]][cities[i]] = features.CITIES[key][cities[i]]
        else:
            self.hands = hands
        for i in range(0, len(self.players)):
            self.players[i][1] = self.players[i][1].init(copy.deepcopy(self.board),
                                                         features, self.players[i][0],
                                                         self.hands)

    def take_turn(self):
        """ Take exactly one turn """
        move = self.players[self.board.turn][1].move(copy.deepcopy(self.board))
        self.board.make_move(move, self.board.turn)
        return self.board.is_terminal(self.hands)

    def make_move(self, move, player):
        """ Make a move for one player """
        return self.board.make_move(move, player)

    def play_game(self, window=None, prompt=False):
        """ Play a whole game """

        while not self.board.is_terminal(self.hands):
            if window:
                window.draw(self.board, self.hands)
                window.draw_turn(int((self.board.total_turns / len(self.players)) + 1),
                                 self.board.turn + 1, self.board.tracks_left)
                if self.board.total_turns >= len(self.players):
                    window.draw_standings(self.board.get_totals(self.hands))

            if prompt:
                if not util.wait_for_key():
                    break

            self.take_turn()
