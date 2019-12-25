#!/usr/bin/python3
""" Tracks various states about the current game session """
import features

POINTS = 0x0001
TRACKS = 0x0002
SELECT = 0x0004
ALL = POINTS|TRACKS|SELECT

class State:
    """
      Provides utility information about a Trans America game state.

      It provides a range of information about the game state,
      which can be configured, so AIs that want to avoid the overhead
      in this module can disable those computations.

    """
    def __init__(self, desired, board, num_players, window=None):
        """ Constructs the game state """
        self.board = board
        self.desired_states = desired
        self.num_players = num_players
        self.hubs = []
        self.window = window

        if self.desired_states & POINTS:
            self.points = []

        if self.desired_states & TRACKS:
            self.tracks = set()

        for _ in range(0, num_players):
            self.hubs.append(None)
            self.points.append(set())

        if self.desired_states & SELECT:
            self.construct_select_costs()

            # player_nodes_in_reach:  move tracking for where a player can move next
            #  Has 3 sets per player: Nodes within a 0 cost edge of the hub, nodes within 1 cost
            #   of the hub and nodes within a 2 cost edge of the hub, at indices [0], [1], and [2]
            self.player_nodes_in_reach = []
            for _ in range(0, self.num_players):
                self.player_nodes_in_reach.append([set(), set(), set()])

            # distances_left:  track interesting locations for each player
            #   Dictionary per player of locations and minimum tracks to reach them from the hub.
            #   Includes using other player's track.
            self.distances_left = []


    # Naive state tracking.  The most basic game play only requires that we know
    #  where players have moved so we can determine if the game is over.
    # The points and tracks are that naive state
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

    def record_hub(self, mover, move):
        """ Take note of a player choosing a hub """
        self.hubs[mover] = move
        if self.desired_states & POINTS:
            self.add_one_point(mover, move)

        if self.desired_states & SELECT:
            self.update_select_hub(mover, move)

    def record_move(self, mover, move):
        """ Take note of a player making a move """
        if self.desired_states & POINTS:
            self.add_one_point(mover, move[0])
            self.add_one_point(mover, move[1])

        if self.desired_states & TRACKS:
            self.add_track(move[0], move[1])
            self.add_track(move[1], move[0])

        if self.desired_states & SELECT:
            self.update_select_move(mover, move)

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

    # Select cost optimization
    #   As a first order of providing more information to AIs, it is
    # useful to track select costs.  These functions manage that.
    def construct_select_costs(self):
        """ select_costs are costs between nodes we care about.
            We mostly care about cities, hubs, and nearby nodes.
            It's an optimized set of costs; we only store 'down and right'
            costs; since it's a mirror, if you want to know the cost
            of a point 'up and left', you ask what the cost from it to
            you is instead
        """
        self.select_costs = []
        for i in range(0, features.LAST_ROW):
            self.select_costs.append([])
            for _ in range(0, features.LAST_COLUMN):
                self.select_costs[i].append([[0, 1], [1, 1]])

        for mountain in features.MOUNTAINS_AND_RIVERS:
            self.set_select_cost(mountain[0], mountain[1], 2)
        for ocean in features.OCEANS:
            for neighbor in self.get_select_neighbors(ocean):
                self.set_select_cost(ocean, neighbor[0], 3)

    def get_select_cost(self, point1, point2):
        """ Cost to get from point 1 to point 2 for selected points """
        offset = sum((point1[0]-point2[0], point1[1]-point2[1]))
        if offset < 0:
            change = (point2[0]-point1[0], point2[1]-point1[1])
            return self.select_costs[point1[0]][point1[1]][change[0]][change[1]]
        if offset > 0:
            change = (point1[0]-point2[0], point1[1]-point2[1])
            return self.select_costs[point2[0]][point2[1]][change[0]][change[1]]
        return 0

    def set_select_cost(self, point1, point2, cost):
        """ Sets the path cost from point1 to point2 for selected paths """
        offset = sum((point1[0]-point2[0], point1[1]-point2[1]))
        if offset < 0:
            change = (point2[0]-point1[0], point2[1]-point1[1])
            self.select_costs[point1[0]][point1[1]][change[0]][change[1]] = cost
        elif offset > 0:
            change = (point1[0]-point2[0], point1[1]-point2[1])
            self.select_costs[point2[0]][point2[1]][change[0]][change[1]] = cost

    def get_select_neighbors(self, point, mincost=1, maxcost=2):
        """ Returns neighors with cost between mincost and maxcost of a given node """
        neighbors = []
        if point[0]+1 < len(self.select_costs):
            if point[1]+1 < len(self.select_costs[0]):
                cost = self.select_costs[point[0]][point[1]][1][1]
                if mincost <= cost <= maxcost:
                    neighbors.append(((point[0]+1, point[1]+1), cost))
            cost = self.select_costs[point[0]][point[1]][1][0]
            if mincost <= cost <= maxcost:
                neighbors.append(((point[0]+1, point[1]), cost))
        if point[1]+1 < len(self.select_costs[0]):
            cost = self.select_costs[point[0]][point[1]][0][1]
            if mincost <= cost <= maxcost:
                neighbors.append(((point[0], point[1]+1), cost))
        if point[0] > 0:
            if point[1] > 0:
                cost = self.select_costs[point[0]-1][point[1]-1][1][1]
                if mincost <= cost <= maxcost:
                    neighbors.append(((point[0]-1, point[1]-1), cost))
            cost = self.select_costs[point[0]-1][point[1]][1][0]
            if mincost <= cost <= maxcost:
                neighbors.append(((point[0]-1, point[1]), cost))
        if point[1] > 0:
            cost = self.select_costs[point[0]][point[1]-1][0][1]
            if mincost <= cost <= maxcost:
                neighbors.append(((point[0], point[1]-1), cost))
        return neighbors

    # Select move optimization
    #   As another optimization, it is helpful to track moves that
    # are available to a player, along with interesting places a given
    # player can reach.
    def fast_get_moves(self, hub, tracks_left):
        """ If we are tracking moves, we can more quickly find a set of legal moves """
        moves = set()
        if hub is None:
            for i in range(0, self.board.row):
                for j in range(0, self.board.cols):
                    if len(self.get_select_neighbors((i, j))) != 0:
                        moves.add((i, j))
            return moves

        player = 0
        for i in range(0, len(self.player_nodes_in_reach)):
            if hub in self.player_nodes_in_reach[i][0]:
                player = i
                break
        for move in self.player_nodes_in_reach[player][1]:
            for neighbor in self.get_select_neighbors(move, 1, 1):
                if neighbor[0] in self.player_nodes_in_reach[player][0]:
                    moves.add((move, neighbor[0]))
                    break
        if tracks_left == 2:
            for move in self.player_nodes_in_reach[player][2]:
                for neighbor in self.get_select_neighbors(move, 2, 2):
                    if neighbor[0] in self.player_nodes_in_reach[player][0]:
                        moves.add((move, neighbor[0]))
                        break
        return moves

    def update_select_hub(self, player, move):
        """ Update our selected move and cost information based on a new hub """
        reachable = self.get_select_neighbors(move)
        self.player_nodes_in_reach[player][0].add(move)
        for i in range(0, len(reachable)):
            self.player_nodes_in_reach[player][reachable[i][1]].add(reachable[i][0])

        self.distances_left.append({})
        for city in self.board.cities.values():
            for location in city.values():
                self.distances_left[player][location] = self.board.get_cost(move, location)
        for j in range(0, player+1):
            hub = self.hubs[j]
            if hub is None:
                continue
            self.distances_left[player][hub] = self.board.get_cost(move, hub)
            self.distances_left[j][move] = self.board.get_cost(move, hub)

    def update_select_move(self, player, move):
        """ Update our selected move and cost information based on a new move """
        cost = self.get_select_cost(move[0], move[1])
        self.set_select_cost(move[0], move[1], 0)
        for track in move:
            if track not in self.player_nodes_in_reach[player][0]:
                #Update distances for this track placement.This uses a Floyd-Warshall like algorithm
                for i in range(0, len(self.hubs)):
                    if i == player:
                        continue
                    hub = self.hubs[i]
                    if self.distances_left[player][hub] > 0:
                        for compare_track in self.player_nodes_in_reach[i][0]:
                            if self.board.get_cost(track, compare_track) < self.distances_left[player][hub]:
                                self.distances_left[player][hub] = self.board.get_cost(track, compare_track)
                            if self.board.get_cost(track, compare_track) < self.distances_left[i][self.hubs[player]]:
                                self.distances_left[i][self.hubs[player]] = self.board.get_cost(track, compare_track)

                for city in self.board.cities.values():
                    for location in city.values():
                        if self.board.get_cost(track, location) < self.distances_left[player][location]:
                            self.distances_left[player][location] = self.board.get_cost(track, location)

                for i in range(0, len(self.hubs)):
                    for j in range(0, len(self.hubs)):
                        if self.distances_left[j][self.hubs[player]]+self.distances_left[player][self.hubs[i]] < self.distances_left[j][self.hubs[i]]:
                            self.distances_left[j][self.hubs[i]] = self.distances_left[j][self.hubs[player]]+self.distances_left[player][self.hubs[i]]
                        if self.distances_left[i][self.hubs[player]]+self.distances_left[player][self.hubs[j]] < self.distances_left[i][self.hubs[j]]:
                            self.distances_left[i][self.hubs[j]] = self.distances_left[i][self.hubs[player]]+self.distances_left[player][self.hubs[j]]
                    for city in self.board.cities.values():
                        for location in city.values():
                            if self.distances_left[i][location] > self.distances_left[player][location]+self.distances_left[i][self.hubs[player]]:
                                self.distances_left[i][location] = self.distances_left[player][location]+self.distances_left[i][self.hubs[player]]
                            if self.distances_left[player][location] > self.distances_left[i][location]+self.distances_left[player][self.hubs[i]]:
                                self.distances_left[player][location] = self.distances_left[i][location]+self.distances_left[player][self.hubs[i]]

                #Update set of possible moves
                if track in self.player_nodes_in_reach[player][cost]:
                    self.player_nodes_in_reach[player][cost].remove(track)
                self.player_nodes_in_reach[player][0].add(track)
                reachable = self.get_select_neighbors(track)
                for i in range(0, len(reachable)):
                    node = reachable[i][0]
                    worth = True
                    for j in range(0, reachable[i][1]):
                        if node in self.player_nodes_in_reach[player][j]:
                            worth = False
                            break
                    if worth:
                        self.player_nodes_in_reach[player][reachable[i][1]].add(node)
                    for k in range(reachable[i][1]+1, 3):
                        if node in self.player_nodes_in_reach[player][k]:
                            self.player_nodes_in_reach[player][k].remove(node)

                #Note that if we hit another player, we need to union the possible moves
                for i in range(0, len(self.player_nodes_in_reach)):
                    if i == player:
                        continue
                    elif track in self.player_nodes_in_reach[i][0]:
                        for j in range(0, 3):
                            self.player_nodes_in_reach[player][j].update(self.player_nodes_in_reach[i][j])
                            self.player_nodes_in_reach[i][j] = self.player_nodes_in_reach[player][j]

        #Apparently we do it twice, because better safe than sorry.
        for i in range(0, len(self.player_nodes_in_reach)):
            if i == player:
                continue
            for track in move:
                if track in self.player_nodes_in_reach[i][0]:
                    for j in range(0, 3):
                        self.player_nodes_in_reach[player][j].update(self.player_nodes_in_reach[i][j])
                        self.player_nodes_in_reach[i][j] = self.player_nodes_in_reach[player][j]
                    self.player_nodes_in_reach[player][2].difference_update(self.player_nodes_in_reach[player][1])
                    self.player_nodes_in_reach[player][2].difference_update(self.player_nodes_in_reach[player][0])
                    self.player_nodes_in_reach[player][1].difference_update(self.player_nodes_in_reach[player][0])

    def eval_move(self, player, move, distances_left):
        """
        Computes a move's effect on all total distances without actually making the move. Note that this does modify distances_left.
        This logic is the same as the update logic for make_move,  but doesn't actually modify the board.
        The actual algorithm is similar to Floyd-Warshall,  but on just the cities and hubs.
        """
        #This for loop simply finds the node that the player isn't already connected to in the move.
        for track in move:
            if track not in self.player_nodes_in_reach[player][0]:
                #Use cost matrix to update player to player costs if this track is closer than any previous track.
                for i in range(0, len(self.hubs)):
                    if i == player:
                        continue
                    hub = self.hubs[i]
                    if distances_left[player][hub] > 0:
                        for compare_track in self.player_nodes_in_reach[i][0]:
                            if self.board.get_cost(track, compare_track) < distances_left[player][hub]:
                                distances_left[player][hub] = self.board.get_cost(track, compare_track)
                            if self.board.get_cost(track, compare_track) < distances_left[i][self.hubs[player]]:
                                distances_left[i][self.hubs[player]] = self.board.get_cost(track, compare_track)

                #Update any cities that this track brings me closer to
                for city in self.board.cities.values():
                    for location in city.values():
                        if self.board.get_cost(track, location) < distances_left[player][location]:
                            distances_left[player][location] = self.board.get_cost(track, location)
                #Update any cities/hubs that are faster to reacher via another player
                for i in range(0, len(self.hubs)):
                    for j in range(0, len(self.hubs)):
                        if distances_left[j][self.hubs[player]]+distances_left[player][self.hubs[i]] < distances_left[j][self.hubs[i]]:
                            distances_left[j][self.hubs[i]] = distances_left[j][self.hubs[player]]+distances_left[player][self.hubs[i]]
                        if distances_left[i][self.hubs[player]]+distances_left[player][self.hubs[j]] < distances_left[i][self.hubs[j]]:
                            distances_left[i][self.hubs[i]] = distances_left[i][self.hubs[player]]+distances_left[player][self.hubs[j]]
                    for city in self.board.cities.values():
                        for location in city.values():
                            if distances_left[player][location] > distances_left[i][location]+distances_left[player][self.hubs[i]]:
                                distances_left[player][location] = distances_left[i][location]+distances_left[player][self.hubs[i]]
                            if distances_left[i][location] > distances_left[player][location]+distances_left[i][self.hubs[player]]:
                                distances_left[i][location] = distances_left[player][location]+distances_left[i][self.hubs[player]]
        return distances_left

    def value(self, hands):
        """ Get the value of a hand """
        for player, hand in enumerate(hands):
            player_done = True
            for city in hand.values():
                if city not in self.player_nodes_in_reach[player][0]:
                    player_done = False
                    break
            if player_done:
                return player
        return None

    def is_terminal(self, hands):
        """ Is the player finished? """
        if self.value(hands) is None:
            return False
        return True

    def get_totals(self, hands):
        """ Get total distance to go """
        totals = []
        for i in range(0, len(hands)):
            totals.append(0)
            for city in hands[i].values():
                totals[i] += self.distances_left[i][city]
        return totals

def unit_test():
    """ Unit tests for this module """

if __name__ == '__main__':
    unit_test()
