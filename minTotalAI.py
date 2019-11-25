import board as b
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
        self.hub=None
        self.board=board
        for city in self.hands[self.name].values():
            self.cities.append(city)
        self.costs=copy.deepcopy(b.costs[self.cities[0][0]][self.cities[0][1]])
        
        for city in self.cities[1:]:
            for i in range(0,self.board.size()[0]):
                for j in range(0,self.board.size()[1]):
                    self.costs[i][j]+=b.costs[city[0]][city[1]][i][j]

    
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
            return minspot
        possibleMoves=list(board.get_moves(self.hub))
        values=[]
        for move in possibleMoves:
            state=[]
            tempdistances=copy.deepcopy(board.distances_left)
            tempdistances=self.eval_move(board.turn,move,board,tempdistances)
            for i in range(0,len(self.cities)):
                total=tempdistances[self.name][self.cities[i]]
                state.append(total)
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(sum(values[i])<sum(values[bestMove])):
                bestMove=i
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

