#Protip: Don't name your variables board
import board as b
import board
import random
import copy

#This is a copy of the logic that updates minimum distances for each player to each city. It is used to evaluate moves without needing to copy the state.
from minDifferenceAI import eval_move

#Obvious FOO strategy AI. Simply place whatever track reduces the cost to all of your cities the most
def init(board,features,me,hands):
    return minTotalAI(board,features,me,hands)

class minTotalAI:
    def __init__(self,board,features,me,hands):
        self.name=me
        self.features=features
        self.hands=hands
        self.cities=[]
        self.costs=[]
        self.hub=None
        self.board=board

        #Need to compute initial totals for each possible hub placement.
        for city in self.hands[self.name].values():
            self.cities.append(city)
        self.costs=copy.deepcopy(b.costs[self.cities[0][0]][self.cities[0][1]])
        for city in self.cities[1:]:
            for i in range(0,self.board.size()[0]):
                for j in range(0,self.board.size()[1]):
                    self.costs[i][j]+=b.costs[city[0]][city[1]][i][j]

    #Move function
    def move(self,board):
        #Place the hub first
        if(self.hub==None):
            minspot=None
            mincost=None
            for i in range(0,self.board.size()[0]):
                for j in range(0,self.board.size()[1]):
                    if(minspot==None):
                        minspot=(i,j)
                        mincost=self.costs[i][j]
                    elif(self.costs[i][j]<mincost):
                        minspot=(i,j)
                        mincost=self.costs[i][j]
            self.hub=minspot
            return minspot

        #After, look at all the possible moves, and compute their impact on the total by aggregating eval_move (which doesn't modify state). Return the best one.
        possibleMoves=list(board.get_moves(self.hub))
        values=[]
        for move in possibleMoves:
            state=[]
            tempdistances=copy.deepcopy(board.distances_left)
            tempdistances=eval_move(board.turn,move,board,tempdistances)
            for i in range(0,len(self.cities)):
                total=tempdistances[self.name][self.cities[i]]
                state.append(total)
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(sum(values[i])<sum(values[bestMove])):
                bestMove=i
        return possibleMoves[bestMove]

