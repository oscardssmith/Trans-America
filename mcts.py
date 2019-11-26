from copy import copy, deepcopy
from math import sqrt
import math
import random

# This mcts code is way ugly because you sometimes place 2 tracks -> make 2 moves in a row, so backprop
# gets really nasty
from minDifferenceAI import eval_move #used for fpu

UCB_CONST = .75
hands = None

class Node:
    """Node used in MCTS"""
    def __init__(self, state, parent_node, turn):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.parent = parent_node
        self.turn = turn
        self.children = {} # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.unexpanded = list(state.get_moves(state.hubs[state.turn])) # Stores unvisited moves to speed up search
        self.unexpanded.sort(key = lambda x: self.fpu(x,state))
        self.visits = 0
        self.value = 0
        self.heuristic = heuristic_value(state, self.turn)

    def addMove(self, state, move, turn):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move in self.unexpanded:
            self.children[move] = Node(state, self, turn)
            del self.unexpanded[-1]
            return True
        print('Yikes')
        return False

    def updateValue(self, outcome, root_player):
        """Updates the value estimate for the node's state.
        outcome: +1 for we win, -1 for they win"""
        self.visits += 1
        n = self.visits
        factor = (root_player==self.turn)*2-1
        self.value = self.value * (n-1)/n + factor*outcome/n
        if self.parent is not None:
            self.parent.updateValue(outcome, root_player)

    def UCBWeight(self):
        """Weight from the UCB formula used by parent to select a child.
        This node will be selected by parent with probability proportional
        to its weight."""
        return (self.value + 
               self.heuristic/self.visits +
               sqrt(sqrt(self.parent.visits)/self.visits) * UCB_CONST)
    
    def fpu(self, move, state):
        tempdistances=deepcopy(state.distances_left)
        tempdistances=eval_move(state.turn,move,state,tempdistances)
        difference = 0
        global hands
        for city in hands[self.turn].values():
            difference += tempdistances[self.turn][city]
        for city in hands[1-self.turn].values():
            difference -= tempdistances[1-self.turn][city]
        return difference
        
    def __lt__(self, other):
        ''' Overrides < so that max works. '''
        return self.UCBWeight() < other.UCBWeight()

def init(board,features,me,hands):
    return mctsAI(board,features,me,hands)

def heuristic_value(state, me):
    global hands
    totals = state.get_totals(hands)
    return (totals[1-me]-totals[me])/5


class mctsAI:
    def __init__(self,board,features,me,hands):
        self.name=me
        self.me=me
        #self.features=features
        self.hands=hands
        self.hub= None
        #self.board=board
        self.first_move = True
        
    def move(self, state, rollouts=400):
        """Select a move by Monte Carlo tree search.
        Plays rollouts random games from the root node to a terminal state.
        In each rollout, play proceeds according to UCB while all children have
        been expanded. The first node with unexpanded children has a random child
        expanded. After expansion, play proceeds by selecting uniform random moves.
        Upon reaching a terminal state, values are propagated back along the
        expanded portion of the path. After all rollouts are completed, the move
        generating the highest value child of root is returned.
        Inputs:
            node: the node for which we want to find the optimal move
            state: the state at the root node
            rollouts: the number of root-leaf traversals to run
        Return:
            The legal move from node.state with the highest value estimate
        """
        
        
        # Hard code initial hub placement because it's OK
        if self.first_move:
            global hands
            hands = self.hands
            self.first_move = False
            for i, loc in enumerate(self.hands[self.me].values()):
                if i >= 3 and loc not in state.hubs:
                    break
            self.hub = loc
            return self.hub
        
        root = Node(state, None, 1-self.me)
        me = self.name
        for i in range(rollouts):
            new_state = deepcopy(state)
            leaf = self.representative_leaf(root, new_state) #deepcopy to not overwrite root state

            value = self.rollout(new_state)
            leaf.updateValue(value, self.me)
        if root.visits < 1:
            return random_move(root)
        children = root.children
        best_move = max(children, key=lambda move: children[move].value)
        return best_move

    def representative_leaf(self, node, state):
        ''' Picks a leaf node by descending the tree.
            Creates a new leaf and returns it (and mutates state to be the state at that leaf). '''
        while True:
            children = node.children
            if len(node.unexpanded):
                move = node.unexpanded[-1]
                turn = deepcopy(state.turn)
                state.make_move(move, state.turn, True)
                node.addMove(state, move, turn)
                return children[move]
            if state.is_terminal(self.hands):
                return node
            best_move = max(children, key=lambda move: children[move])
            state.make_move(best_move, state.turn, True)
            node = children[best_move]
    
    def rollout(self, state):
        ''' We stopped using real rollouts because they were slow and inaccurate. '''
        
        return heuristic_value(state, self.me)
        #while not state.is_terminal(self.hands):
        #    moves = state.get_moves(self.hub)
        #    state.make_move(random.sample(moves, 1)[0], state.turn, False)
        #return (state.value(self.hands) == self.me)*2 -1

