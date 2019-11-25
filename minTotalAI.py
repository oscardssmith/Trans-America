import board
import random
import copy

def init(board,features,me,hands):
    return minTotalAI(board,features,me,hands)

class minTotalAI:
    
    def __init__(self,board,features,me,hands):
        self.name=me
        self.features=features
        self.hands=hands
        self.cities=[]
        self.costs=[]
        self.city_costs=[]
        self.hub=None
        self.board=board
        for city in self.hands[self.name].values():
            self.cities.append(city)
        self.costs=self.board.costs[self.cities[0][0]][self.cities[0][1]]
        
        for city in self.cities[1:]:
            for i in range(0,self.board.size()[0]):
                for j in range(0,self.board.size()[1]):
                    self.costs[i][j]+=self.board.costs[city[0]][city[1]][i][j]

        print(self.costs)
    
    def move(self,board):
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
            for city in self.cities:
                self.city_costs.append(board.costs[minspot[0]][minspot[1]][city[0]][city[1]])
            return minspot
        #print(self.hub)
        possibleMoves=board.get_moves(self.hub)
        values=[]
        for move in possibleMoves:
            state=[]
            for i in range(0,len(self.cities)):
                total=self.city_costs[i]
                for track in move:
                    for spot in track:
                        #tempcosts=board.computeCosts(spot)
                        if(board.costs[spot[0]][spot[1]][self.cities[i][0]][self.cities[i][1]]<total):
                            total=board.costs[spot[0]][spot[1]][self.cities[i][0]][self.cities[i][1]]
                state.append(total)
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(sum(values[i])<sum(values[bestMove])):
                bestMove=i
        self.city_costs=values[bestMove]
        print(possibleMoves[bestMove])
        return possibleMoves[bestMove]
