import board as b
import board
import random
import copy

temp=0

#Another simple AI. Minimize my cost - opponent cost. Currently only works single player, but that's okay.
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
        self.hub=None
        self.board=board
        self.min_all=min_all

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
                        if(self.min_all):
                            state=state-min(tempdistances[player][city],tempdistances[self.name][city])
                        else:
                            state=state-tempdistances[player][city]
            values.append(state)
        bestMove=0
        for i in range(0,len(possibleMoves)):
            if(values[i]<values[bestMove]):
                bestMove=i
        return possibleMoves[bestMove]


#Computes a move's effect on all total distances without actually making the move. Note that this does modify distances_left.
#This logic is the same as the update logic for make_move, but doesn't actually modify the board.
#The actual algorithm is similar to Floyd-Warshall, but on just the cities and hubs.
def eval_move(playerNum,move,board,distances_left):
    #This for loop simply finds the node that the player isn't already connected to in the move.
    for track in move:
        if(track not in board.player_nodes_in_reach[playerNum][0]):
            #Use cost matrix to update player to player costs if this track is closer than any previous track.
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
            #Update any cities that this track brings me closer to
            for city in board.cities.values():
                for location in city.values():
                    if(b.costs[track[0]][track[1]][location[0]][location[1]]<distances_left[playerNum][location]):
                        distances_left[playerNum][location]=b.costs[track[0]][track[1]][location[0]][location[1]]
            #Update any cities/hubs that are faster to reacher via another player
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

