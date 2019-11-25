import board as b
import board
import random
import copy

temp=0

def init(board,features,me,hands):
    min_all=False
    if(temp==me):
        #print(me)
        #min_all=True
        pass
    return minDifferenceAI(board,features,me,hands,min_all)

class minDifferenceAI:
    
    def __init__(self,board,features,me,hands,min_all=False):
        self.name=me
        self.features=features
        self.hands=hands
        self.cities=[]
        self.costs=[]
        self.city_costs=[]
        self.hub=None
        self.board=board
        self.min_all=min_all
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
                self.city_costs.append(b.costs[minspot[0]][minspot[1]][city[0]][city[1]])
            return minspot
        #print(self.hub)
        possibleMoves=list(board.get_moves(self.hub))
        #print(len(possibleMoves))
        values=[]
        for move in possibleMoves:
            state=0
            tempdistances=copy.deepcopy(board.distances_left)
            tempdistances=self.eval_move(board.turn,move,board,tempdistances)
            for i in range(0,len(self.cities)):
                state+=tempdistances[self.name][self.cities[i]]
            for player in self.hands.keys():
                if(player!=self.name):
                    for city in self.hands[player].values():
                        if(self.min_all):
                            state=state-min(tempdistances[player][city],tempdistances[self.name][city])
                        else:
                            state=state-tempdistances[player][city]
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(values[i]<values[bestMove]):
                bestMove=i
        self.city_costs=values[bestMove]
        #print(values,bestMove)
        #print(possibleMoves[bestMove])
        return possibleMoves[bestMove]

    def eval_move(self,playerNum,move,board,distances_left):
        for track in move:
            if(track not in board.player_nodes_in_reach[self.name][0]):
            #Update distances for this track placement
                for i in range(0,len(board.hubs)):
                    if(i==playerNum):
                        continue
                    hub=board.hubs[i]
                    if(distances_left[playerNum][hub]>0):
                        for compare_track in board.player_nodes_in_reach[i][0]:
                            if(b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]<distances_left[playerNum][hub]):
                                distances_left[playerNum][hub]=b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
                            if(b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]<distances_left[i][board.hubs[playerNum]]):
                                distances_left[i][board.hubs[playerNum]]=b.costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
                for city in board.cities.values():
                    for location in city.values():
                        if(b.costs[track[0]][track[1]][location[0]][location[1]]<distances_left[playerNum][location]):
                            distances_left[playerNum][location]=b.costs[track[0]][track[1]][location[0]][location[1]]
                for i in range(0,len(board.hubs)):
                    for j in range(0,len(board.hubs)):
                        if(distances_left[j][board.hubs[playerNum]]+distances_left[playerNum][board.hubs[i]]<distances_left[j][board.hubs[i]]):
                            distances_left[j][board.hubs[i]]=distances_left[j][board.hubs[playerNum]]+distances_left[playerNum][board.hubs[i]]
                        if(distances_left[i][board.hubs[playerNum]]+distances_left[playerNum][board.hubs[j]]<distances_left[i][board.hubs[j]]):
                            distances_left[i][board.hubs[i]]=distances_left[i][board.hubs[playerNum]]+distances_left[playerNum][board.hubs[j]]
                    for city in board.cities.values():
                        for location in city.values():
                            if(distances_left[playerNum][location]>distances_left[i][location]+distances_left[playerNum][board.hubs[i]]):
                                distances_left[playerNum][location]=distances_left[i][location]+distances_left[playerNum][board.hubs[i]]
                            if(distances_left[i][location]>distances_left[playerNum][location]+distances_left[i][board.hubs[playerNum]]):
                                distances_left[i][location]=distances_left[playerNum][location]+distances_left[i][board.hubs[playerNum]]
        return distances_left

