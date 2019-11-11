import board
import mapFeatures
import random
import copy

class minTotalAI:
    hand = []
    handnames=[]
    costs = None
    hub=[]
    tracks = []
    moves = []
    
    def __init__(self,board,cities):
        for key in cities.keys():
            values=[]
            for i in cities[key].keys():
                values.append(i)
            choice=random.choice(values)
            self.handnames.append(choice)
            self.hand.append(cities[key][choice])
        print(self.handnames)
        print(self.hand)
        self.costs=None
        for city in self.hand:
            if(self.costs==None):
                self.costs=copy.deepcopy(board.costs[city[0]][city[1]])
            else:
                for i in range(0,len(board.costs[city[0]][city[1]])):
                    for j in range(0,len(board.costs[city[0]][city[1]][0])):
                        self.costs[i][j]+=board.costs[city[0]][city[1]][i][j]
        mymin=None
        for row in range(0,len(self.costs)):
            for column in range(0,len(self.costs[0])):
                if(mymin==None):
                    mymin=self.costs[row][column]
                elif(mymin>self.costs[row][column]):
                    self.hub=[(row,column)]
                    mymin=self.costs[row][column]
                elif(mymin==self.costs[row][column]):
                    self.hub.append((row,column))
        self.hub=random.choice(self.hub)
        self.costs=copy.deepcopy(board.costs[self.hub[0]][self.hub[1]])
        print(self.hub)
    
    #def make_move(self,board):
     #   board.costs[move[0]][move[1]]
        

