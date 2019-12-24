#!/usr/bin/python3
""" Represents a map of TransAmerica """
import queue
import features

class Board:
    """
      Represent the Trans America map.  The key here is to keep
      an array of costs from each node to each other node.

      See features for a little more description of the mathematical
      representation of a map.

      The costs array will provide the distance from any point
      to any other point.  A game will have a 'static' map which will
      represent a blank game board, and what it would take to move
      from any position to any other position on the board, using a flood
      fill algorithm to determine optimal path.

    """
    def __init__(self):
        """ Constructs the board map """
        self.mountains_and_rivers = features.MOUNTAINS_AND_RIVERS
        self.oceans = features.OCEANS
        self.cols = features.LAST_COLUMN
        self.rows = features.LAST_ROW
        self.cities = features.CITIES
        self.costs = []

        # Set up default costs
        for row in range(0, self.rows):
            self.costs.append([])
            for col in range(0, self.cols):
                self.costs[row].append(self.default_cost(row, col))

        # Mountains and rivers cost a bit more
        for mountain in self.mountains_and_rivers:
            self.set_cost(mountain[0], mountain[1], 2)
            self.set_cost(mountain[1], mountain[0], 2)

        # Oceans go back to being impossible
        for ocean in features.OCEANS:
            for neighbor in self.get_neighbors(ocean):
                self.set_cost(ocean, neighbor[0], self.cols * self.rows)
                self.set_cost(neighbor[0], ocean, self.cols * self.rows)

        # Now do a search to lower costs
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                self.compute_costs(row, col)

    def default_cost(self, row, col):
        """ Set up a default cost from every point to every other point """
        costs = []
        for i in range(0, self.rows):
            costs.append([])
            for j in range(0, self.cols):
                # We do 0 for ourselves, or absurdly large, which will trigger a recompute
                if row == i and col == j:
                    costs[i].append(0)
                elif self.is_neighbor((row, col), (i, j)):
                    costs[i].append(1)
                else:
                    costs[i].append(2 * self.rows * self.cols)
        return costs

    def is_neighbor(self, point1, point2): # pylint: disable=R0201
        """ We simulate a hex grid by using a coordinate system such
            that the offsets +1, -1 and -1, +1 are not allowed """
        row = point1[0] - point2[0]
        col = point1[1] - point2[1]

        # You cannot be your own neighbor
        if col == 0 and row == 0:
            return False

        # +1, +1  +1, +0, +0, +1
        if 0 <= row <= 1 and 0 <= col <= 1:
            return True

        # -1, -1  -1, -0, -0, -1
        if -1 <= row <= 0 and -1 <= col <= 0:
            return True

        return False

    def get_cost(self, point1, point2):
        ''' Cost to get from point 1 to point 2'''
        return self.costs[point1[0]][point1[1]][point2[0]][point2[1]]

    def set_cost(self, point1, point2, cost):
        ''' Sets the path cost (used in make_move)'''
        self.costs[point1[0]][point1[1]][point2[0]][point2[1]] = cost

    def get_neighbors(self, point, mincost=1, maxcost=2):
        """ Get all of our neighbors within a certain cost range """
        neighbors = []
        for row in range(-1, 1 + 1):
            if point[0] + row >= self.rows or point[0] + row < 0:
                continue
            for col in range(-1, 1 + 1):
                if point[1] + col >= self.cols or point[1] + col < 0:
                    continue

                possible_neighbor = (point[0] + row, point[1] + col)
                if self.is_neighbor(point, possible_neighbor):
                    cost = self.get_cost(point, possible_neighbor)
                    if mincost <= cost <= maxcost:
                        neighbors.append((possible_neighbor, cost))
        return neighbors

    def compute_costs(self, row, col):
        ''' Computes costs to a point using BFS '''
        check = queue.PriorityQueue()
        for neighbor in self.get_neighbors([row, col]):
            for nextdoor in self.get_neighbors(neighbor[0]):
                if nextdoor[0][0] == row and nextdoor[0][1] == col:
                    continue

                check.put((0, nextdoor[0]))

        while not check.empty():
            _, test = check.get()
            #print("Testing {} for ({}, {})".format(test, row, col))
            for neighbor in self.get_neighbors(test):
                there = neighbor[0]
                cost = neighbor[1]
                origin_to_here = self.costs[row][col][test[0]][test[1]]
                origin_to_neighbor = self.costs[row][col][there[0]][there[1]]

                if origin_to_here + cost < origin_to_neighbor:
                    self.costs[row][col][there[0]][there[1]] = origin_to_here + cost
                    check.put((origin_to_here + cost, there))

def one_test(mymap, point1, point2, expected, verbose=True):
    """ Run one unit test """
    actual = mymap.costs[point1[0]][point1[1]][point2[0]][point2[1]]
    if actual == expected:
        if verbose:
            print("Okay:  {} -> {} expected {}; actual {}".format(point1, point2, expected, actual))
    else:
        print("Error: {} -> {} expected {}; actual {}".format(point1, point2, expected, actual))

def unit_test():
    """ Unit tests for this module """
    mymap = Board()

    one_test(mymap, (0, 0), (5, 5), 6)
    one_test(mymap, [0, 0], [0, 1], 2)
    one_test(mymap, [0, 0], [1, 1], 2)
    one_test(mymap, [0, 0], [3, 0], 520)
    one_test(mymap, [0, 0], [12, 19], 21)

    one_test(mymap, [5, 7], [5, 2], 7)

    one_test(mymap, [12, 19], [0, 0], 21)
    one_test(mymap, [12, 19], [12, 15], 5)
    one_test(mymap, [12, 19], [2, 17], 10)


if __name__ == '__main__':
    unit_test()
