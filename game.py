""" game.py contains Game control logic for Trans-America """
import random
import copy
import board
import util
import features

class Game:
    ''' class for running a single game. '''

    def __init__(self, players, inboard=None, hands=None):
        self.board = None
        self.turn = 0
        self.tracks_left = 2
        self.players = players
        if inboard is None:
            self.board = board.Board(len(players))
        else:
            self.board = inboard

        if hands is None:
            self.hands = []
            for i in range(0, len(players)):
                self.hands.append({})
            for key, citygroup in features.CITIES.items():
                values = []
                for i in iter(citygroup.keys()):
                    values.append(i)
                cities = random.sample(values, len(self.players))
                for i in range(0, len(self.players)):
                    self.hands[i][key] = features.CITIES[key][cities[i]]
        else:
            self.hands = hands

        for i, player in enumerate(self.players):
            player.start(i, len(self.players), self.hands[i])

    def take_turn(self):
        """ Take exactly one turn """
        if self.turn < len(self.players):
            move = self.players[self.turn].place_hub(copy.deepcopy(self.board))
        else:
            move = self.players[self.turn % len(self.players)].move(copy.deepcopy(self.board),
                                                                    self.tracks_left)
        cost = self.board.make_move(move, self.turn, self.turn % len(self.players))
        self.tracks_left -= cost
        if self.tracks_left == 0:
            self.tracks_left = 2
            self.turn += 1
        return self.board.is_terminal(self.hands)

    def make_move(self, move, player):
        """ Make a move for one player """
        return self.board.make_move(move, player)

    def play_game(self, window=None, prompt=False):
        """ Play a whole game """

        while not self.board.is_terminal(self.hands):
            if window:
                window.draw(self.board, self.hands)
                window.draw_turn(int((self.turn / len(self.players)) + 1),
                                 self.turn + 1, self.tracks_left)
                if self.board.turn >= len(self.players):
                    window.draw_standings(self.board.get_totals(self.hands))

            if prompt:
                if not util.wait_for_key():
                    break

            self.take_turn()
