#!/usr/bin/python3
""" Tracks various states about the current game session """

POINTS = 0x0001
TRACKS = 0x0002
ALL = POINTS|TRACKS

class State:
    """
      Provides utility information about a Trans America game state.

      Initially this provides information about what tracks have
      been placed and what points are in reach by a given player.

    """
    def __init__(self, desired, board, num_players):
        """ Constructs the game state """
        self.board = board
        self.desired_states = desired
        self.num_players = num_players
        self.hubs = []
        self.points = []
        self.tracks = set()
        for _ in range(0, num_players):
            self.hubs.append(None)
            self.points.append(set())


    def add_one_point(self, mover, move):
        """ Add a single point to a per player hash table """
        hashable_move = (move[0] << 8) + move[1]
        self.points[mover].add(hashable_move)
        for player in range(0, self.num_players):
            if player != mover:
                if not self.points[player].isdisjoint(self.points[mover]):
                    self.points[player].add(hashable_move)

    def add_track(self, point1, point2):
        """ Add a single track to a game wide hash table of tracks placed """
        hashed_move = point1[0] << 24 | point1[1] << 16 | \
                      point2[0] << 8 | point2[1]
        self.tracks.add(hashed_move)

    def record_move(self, mover, move):
        """ Record where all the ther moves are """
        if isinstance(move[0], int):
            self.hubs[mover] = move
            if self.desired_states & POINTS:
                self.add_one_point(mover, move)
            return

        self.add_one_point(mover, move[0])
        self.add_one_point(mover, move[1])

        if self.desired_states & TRACKS:
            self.add_track(move[0], move[1])
            self.add_track(move[1], move[0])

    def legal_moves(self, player, mincost=1, maxcost=2):
        """ Return a set of legal moves for this player """
        set_of_moves = set()
        for point in self.points[player]:
            move = (point >> 8, point & 0xff)
            neighbors = self.board.get_neighbors(move, mincost, maxcost)
            for neighbor in neighbors:
                hashed_move = move[0] << 24 | move[1] << 16 | \
                              neighbor[0][0] << 8 | neighbor[0][1]
                if hashed_move not in self.tracks:
                    set_of_moves.add(hashed_move)
        moves = []
        for hashed_move in set_of_moves:
            moves.append(((hashed_move >> 24, (hashed_move >> 16) & 0xff),
                          ((hashed_move >>  8) & 0xff, hashed_move & 0xff)))
        return moves


def unit_test():
    """ Unit tests for this module """

if __name__ == '__main__':
    unit_test()
