import board as b
import board
import random
import copy

#Another simple AI. Minimize my cost - opponent cost. Currently only works single player, but that's okay.
from util import eval_move

def init(board,features,me,hands):
    return minDifferenceAI(board,features,me,hands)

class minDifferenceAI:
    
    def __init__(self,board,features,me,hands):
        self.name=me
        self.features=features
        self.hands=hands
        self.cities=[]
        self.costs=[]
        self.hub=None
        self.board=board

        #Compute my cost - opponent cost for hub placements
        for city in self.hands[self.name].values():
            self.cities.append(city)
        self.costs=copy.deepcopy(b.costs[self.cities[0][0]][self.cities[0][1]])
        for city in self.cities[1:]:
            for i in range(0,self.board.size()[0]):
                for j in range(0,self.board.size()[1]):
                    self.costs[i][j]+=b.costs[city[0]][city[1]][i][j]
        for player in self.hands.keys():
            if(player!=self.name):
                for city in self.hands[player].values():
                    for i in range(0,self.board.size()[0]):
                        for j in range(0,self.board.size()[1]):
                            self.costs[i][j]-=b.costs[city[0]][city[1]][i][j]

    #Move function
    def move(self,board):
        #Place hub
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
        #Get moves, then eval them to see if they improve the differential. Choose move with best differential.
        possibleMoves=list(board.get_moves(self.hub))
        values=[]
        for move in possibleMoves:
            state=0
            tempdistances=copy.deepcopy(board.distances_left)
            tempdistances=eval_move(board.turn,move,board,tempdistances)
            for i in range(0,len(self.cities)):
                state+=tempdistances[self.name][self.cities[i]]
            for player in self.hands.keys():
                if(player!=self.name):
                    for city in self.hands[player].values():
                        state=state-tempdistances[player][city]
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(values[i]<values[bestMove]):
                bestMove=i
        return possibleMoves[bestMove]


