""" game.py contains Game control logic for Trans-America """
import random
import util
import features
from human import Human
from state import State, SELECT

class Game:
    ''' class for running a single game. '''

    def __init__(self, players, board, window=None, hands=None):
        self.board = board
        self.turn = 0
        self.tracks_left = 2
        self.players = players
        self.hubs = []
        self.tracks = []
        self.window = window
        self.state = None

        if hands is None:
            self.hands = self.make_hands(players)
        else:
            self.hands = hands

        states_wanted = 0
        for i, player in enumerate(self.players):
            self.hubs.append(None)
            states_wanted |= player.start(i, len(self.players), board, self.hands[i])

        if states_wanted:
            self.state = State(states_wanted, board, len(self.players), window)


    def make_hands(self, players):
        """ Create a new set of hands """
        hands = []
        for i in range(0, len(players)):
            hands.append({})
        for key, citygroup in features.CITIES.items():
            values = []
            for i in iter(citygroup.keys()):
                values.append(i)
            cities = random.sample(values, len(self.players))
            for i in range(0, len(self.players)):
                hands[i][key] = features.CITIES[key][cities[i]]
        return hands

    def track_is_city(self, track, city):
        """ Helper function to determine if a track connects a city """
        if isinstance(track[0], int):
            return track[0] == city[0] and track[1] == city[1]

        return self.track_is_city(track[0], city) or self.track_is_city(track[1], city)

    def player_done(self, player):
        """ Helper function to determine if a player has reached their cities """
        for i in self.hands[player]:
            found = False
            city = self.hands[player][i]
            for track in self.tracks:
                if self.track_is_city(track, city):
                    found = True
                    break
            if not found:
                return False
        return True

    def is_terminal(self):
        """ Helper function to determine if any player has finished """
        if self.state.desired_states & SELECT:
            return self.state.is_terminal(self.hands)

        for player in range(0, len(self.players)):
            if self.player_done(player):
                return True
        return False


    def record_hub(self, mover, move):
        """ Record a hub placement by a player """
        for player in self.players:
            player.see_hub(mover, move)

        if self.state:
            self.state.record_hub(mover, move)

    def record_move(self, mover, move):
        """ Record the move that just happened """
        self.tracks.append(move)
        if self.window:
            self.window.draw_move(move)

        for player in self.players:
            player.see_move(mover, move)
            if self.state:
                self.state.record_move(mover, move)


    def take_turn(self):
        """ Take exactly one turn """
        player = self.turn % len(self.players)
        if self.turn < len(self.players):
            move = self.players[player].place_hub(self.board, self.state)
            self.record_hub(player, move)
            self.hubs[player] = move
            self.turn += 1
        else:
            move = self.players[player].move(self.board, self.tracks_left, self.state)
            cost = self.board.costs[move[0][0]][move[0][1]][move[1][0]][move[1][1]]
            self.tracks_left -= cost
            self.record_move(player, move)
            if self.tracks_left == 0:
                self.tracks_left = 2
                self.turn += 1

    def play_game(self, prompt=False):
        """ Play a whole game """
        quitting = False
        if self.window:
            self.window.draw_initial(self.board, self.hands)

        while not self.is_terminal():
            player = self.turn % len(self.players)
            if self.window:
                if prompt and not isinstance(self.players[player], Human):
                    self.window.draw_prompt("Press w to proceed, q to quit")
                if self.turn <= len(self.players):
                    self.window.draw_hubs(self.hubs)

                self.window.draw_turn(int(self.turn / len(self.players)) + 1,
                                      player + 1, self.tracks_left)

            if prompt and not isinstance(self.players[player], Human):
                if not util.wait_for_key():
                    quitting = True
                    break

            self.take_turn()

            if self.window:
                if self.turn >= len(self.players):
                    if self.state.desired_states & SELECT:
                        standings = self.state.get_totals(self.hands)
                        self.window.draw_standings(standings)

        if self.window and not quitting:
            util.wait_for_key()
