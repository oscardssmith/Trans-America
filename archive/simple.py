""" Simple AI.  Just place the track that reduces total cost to cities """
import copy
#Protip: Don't name your variables board
import board
import features

#This is a copy of the logic that updates minimum distances for each player to each city.
# It is used to evaluate moves without needing to copy the state.
from util import eval_move

#Obvious FOO strategy AI. Simply place the track to reduce the cost to all of your cities the most
def create():
    """ Return an AI """
    return Simple()

class Simple:
    """ A class to hold the simple minimum total AI algorithm """

    def __init__(self):
        self.num = None
        self.player_count = 0
        self.hand = None
        self.hub = None
        self.cities = []
        self.costs = []

    def start(self, num, player_count, hand):
        """ Construct a simple AI.  Can return a list of features not wanted """
        self.num = num
        self.player_count = player_count
        self.hand = hand
        self.cities = []
        self.costs = []

        #Need to compute initial totals for each possible hub placement.
        for city in self.hand.values():
            self.cities.append(city)
        self.costs = copy.deepcopy(board.costs[self.cities[0][0]][self.cities[0][1]])
        for city in self.cities[1:]:
            for i in range(0, features.LAST_ROW):
                for j in range(0, features.LAST_COLUMN):
                    self.costs[i][j] += board.costs[city[0]][city[1]][i][j]

    def place_hub(self, board_state):
        """ Return where we want out hub """
        minspot = None
        mincost = None
        for i in range(0, features.LAST_ROW):
            for j in range(0, features.LAST_COLUMN):
                if minspot is None:
                    minspot = (i, j)
                    mincost = self.costs[i][j]
                elif self.costs[i][j] < mincost:
                    minspot = (i, j)
                    mincost = self.costs[i][j]
        self.hub = minspot
        return minspot

    def move(self, board_state, tracks_left):
        """ Figure out our move """

        #After,  look at all the possible moves,  and compute their impact on the total by
        # aggregating eval_move (which doesn't modify state). Return the best one.
        board_state.tracks_left = tracks_left
        possible_moves = list(board_state.get_moves(self.hub))
        values = []
        for move in possible_moves:
            state = []
            tempdistances = copy.deepcopy(board_state.distances_left)
            tempdistances = eval_move(self.num, move, board_state, tempdistances)
            for i in range(0, len(self.cities)):
                total = tempdistances[self.num][self.cities[i]]
                state.append(total)
            values.append(state)
        best_move = 0
        for i in range(0, len(possible_moves)):
            if sum(values[i]) < sum(values[best_move]):
                best_move = i
        return possible_moves[best_move]

    def see_move(self, num, move, board_state):
        """ Receive a move made by a player """
