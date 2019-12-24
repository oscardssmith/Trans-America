""" Simple AI.  Just place the track that reduces total cost to cities """
import copy
import features
from template import Template
from state import ALL


#Obvious FOO strategy AI. Simply place the track to reduce the cost to all of your cities the most
def create():
    """ Return an AI """
    return Simple()

class Simple(Template):
    """ A class to hold the simple minimum total AI algorithm """

    def __init__(self):
        super().__init__()
        self.cities = []
        self.costs = []

    def start(self, num, player_count, board, hand):
        """ Construct a simple AI.  Can return a list of features not wanted """
        super().start(num, player_count, board, hand)

        #Need to compute initial totals for each possible hub placement.
        for city in self.hand.values():
            self.cities.append(city)
        self.costs = copy.deepcopy(board.costs[self.cities[0][0]][self.cities[0][1]])
        for city in self.cities[1:]:
            for i in range(0, features.LAST_ROW):
                for j in range(0, features.LAST_COLUMN):
                    self.costs[i][j] += board.costs[city[0]][city[1]][i][j]

        return ALL

    def place_hub(self, board, state): # pylint: disable=W0613
        """ Return where we want out hub """
        minspot = None
        mincost = None
        for i in range(0, board.rows):
            for j in range(0, board.cols):
                if minspot is None:
                    minspot = (i, j)
                    mincost = self.costs[i][j]
                elif self.costs[i][j] < mincost:
                    minspot = (i, j)
                    mincost = self.costs[i][j]
        self.hub = minspot
        return minspot

    def move(self, board, tracks_left, state): # pylint: disable=W0613
        """ Figure out our move """

        #After,  look at all the possible moves,  and compute their impact on the total by
        # aggregating eval_move (which doesn't modify state). Return the best one.
        possible_moves = list(state.fast_get_moves(self.hub, tracks_left))
        values = []
        for move in possible_moves:
            value = []
            tempdistances = copy.deepcopy(state.distances_left)
            tempdistances = state.eval_move(self.num, move, tempdistances)
            for i in range(0, len(self.cities)):
                total = tempdistances[self.num][self.cities[i]]
                value.append(total)
            values.append(value)
        best_move = 0
        for i in range(0, len(possible_moves)):
            if sum(values[i]) < sum(values[best_move]):
                best_move = i
        return possible_moves[best_move]
