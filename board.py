import mapFeatures
import queue

costs=[]

class grid:
    def __init__(self, features,numPlayers,hubs=[]):
        self.turn=0
        self.board=[]
        self.hubs=[]
        self.cities=features.cities
        self.player_nodes_in_reach=[]
        self.distances_left=[]
        self.tracks_left=2
        for i in range(0,numPlayers):
            self.player_nodes_in_reach.append([set(),set(),set()])
        if(len(hubs)==0):
            for i in range(0,numPlayers):
                self.hubs.append(None)
        else:
            self.hubs=hubs
        for i in range(0,13):
            self.board.append([])
            for j in range(0,20):
                self.board[i].append([[0,1],[1,1]])

        for mountain in features.mountains:
            self.set(mountain[0],mountain[1],2)
        for ocean in features.oceans:
            for neighbor in self.get_neighbors(ocean):
                self.set(ocean,neighbor[0],3)
        for i in range(0,13):
            costs.append([])
            for j in range(0,20):
                costs[i].append(self.computeCosts((i,j)))



    def cost(self,point1,point2):
        offset=sum((point1[0]-point2[0],point1[1]-point2[1]))
        if(offset<0):
            change=(point2[0]-point1[0],point2[1]-point1[1])
            return self.board[point1[0]][point1[1]][change[0]][change[1]]
        elif(offset>0):
            change=(point1[0]-point2[0],point1[1]-point2[1])
            return self.board[point2[0]][point2[1]][change[0]][change[1]]

    def set(self,point1,point2,cost):
        offset=sum((point1[0]-point2[0],point1[1]-point2[1]))
        if(offset<0):
            change=(point2[0]-point1[0],point2[1]-point1[1])
            self.board[point1[0]][point1[1]][change[0]][change[1]]=cost
        elif(offset>0):
            change=(point1[0]-point2[0],point1[1]-point2[1])
            self.board[point2[0]][point2[1]][change[0]][change[1]]=cost

    def size(self):
        return (len(self.board),len(self.board[0]))
        
    def get_moves(self,hub):
        if(hub==None):
            for i in range(0,self.size()[0]):
                for j in range(0,self.size()[1]):
                    if(len(self.get_neighbors((i,j)))!=0):
                        moves.add((i,j))
            return moves

        player=0
        for i in range(0,len(self.player_nodes_in_reach)):
            if(hub in self.player_nodes_in_reach[i][0]):
                player=i
                break
        moves = set()
        for move in self.player_nodes_in_reach[player][1]:
            for neighbor in self.get_neighbors(move,1,1):
                if(neighbor[0] in self.player_nodes_in_reach[player][0]):
                    moves.add((move,neighbor[0]))
                    break
            #moves.add(move)
        if(self.tracks_left==2):
            for move in self.player_nodes_in_reach[player][2]:
                for neighbor in self.get_neighbors(move,2,2):
                    if(neighbor[0] in self.player_nodes_in_reach[player][0]):
                        moves.add((move,neighbor[0]))
                        break
        return moves

    def get_neighbors(self,point, mincost=1,maxcost=2):
        neighbors=[]
        if(point[0]+1<len(self.board)):
            if(point[1]+1<len(self.board[0])):
                cost = self.board[point[0]][point[1]][1][1]
                if(cost>=mincost and cost<=maxcost):
                    neighbors.append(((point[0]+1,point[1]+1),cost))
            cost = self.board[point[0]][point[1]][1][0]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0]+1,point[1]),cost))
        if(point[1]+1<len(self.board[0])):
            cost = self.board[point[0]][point[1]][0][1]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0],point[1]+1),cost))
        if(point[0]>0):
            if(point[1]>0):
                cost = self.board[point[0]-1][point[1]-1][1][1]
                if(cost>=mincost and cost<=maxcost):
                    neighbors.append(((point[0]-1,point[1]-1),cost))
            cost = self.board[point[0]-1][point[1]][1][0]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0]-1,point[1]),cost))
        if(point[1]>0):
            cost = self.board[point[0]][point[1]-1][0][1]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0],point[1]-1),cost))
        return neighbors
        

    def LCS(self,point,cutoff,minweight=0):
        visited=[]
        for i in range(0,cutoff+1):
            visited.append({})
        toCheck=queue.PriorityQueue()
        toCheck.put((0,(point,None)))
        visited[0][point]=None
        while(not toCheck.empty()):
            value,track=toCheck.get()
            test=track[0]
            for neighbor in self.get_neighbors(test,minweight,2):
                if(neighbor[1]+value<=cutoff):
                    seen=False
                    for i in visited:
                        if(neighbor[0] in i):
                            seen=True
                            break
                    if(not seen):
                        visited[value+neighbor[1]][neighbor[0]]=test
                        toCheck.put(((neighbor[1]+value),(neighbor[0],test)))
        return visited
    
    def value(self, hands):
        for player, hand in hands.items():
            player_done = True
            for city in hand.values():
                #visited = self.LCS(city,0)[0]
                if city not in self.player_nodes_in_reach[player][0]:
                    player_done = False
                    break
            if player_done:
                return player
        return None
        
    def is_terminal(self, hands):
        if self.value(hands) is None:
            return False
        return True
        
    def computeCosts(self,point):
        out=[]
        for i in range(0,self.size()[0]):
            temp=[]
            for j in range(0,self.size()[1]):
                temp.append(2*self.size()[0]*self.size()[1])
            out.append(temp)
        toCheck=queue.PriorityQueue()
        out[point[0]][point[1]]=0
        toCheck.put((0,point))
        while(not toCheck.empty()):
            value,test=toCheck.get()
            for neighbor in self.get_neighbors(test,0,2):
                if(out[test[0]][test[1]]+neighbor[1]<out[neighbor[0][0]][neighbor[0][1]]):
                    out[neighbor[0][0]][neighbor[0][1]]=out[test[0]][test[1]]+neighbor[1]
                    toCheck.put((out[neighbor[0][0]][neighbor[0][1]],neighbor[0]))
        return out

    def make_move(self,move,playerNum,update=True):
        if(self.turn!=playerNum):
            raise Exception("Stop It")
        if(self.hubs[playerNum]==None):
            self.hubs[playerNum]=move
            reachable=self.get_neighbors(move)
            self.player_nodes_in_reach[playerNum][0].add(move)
            for i in range(0,len(reachable)):
                self.player_nodes_in_reach[playerNum][reachable[i][1]].add(reachable[i][0])
            self.next_turn(2)

            #Compute relevant distances for this hub placement
            if(update):
                self.distances_left.append({})
                for city in self.cities.values():
                    for location in city.values():
                        self.distances_left[playerNum][location]=costs[move[0]][move[1]][location[0]][location[1]]
                for j in range(0,playerNum+1):
                    hub=self.hubs[j]
                    if(hub==None):
                        continue
                    self.distances_left[playerNum][hub]=costs[move[0]][move[1]][hub[0]][hub[1]]
                    self.distances_left[j][move]=costs[move[0]][move[1]][hub[0]][hub[1]]


            return True
        cost=self.cost(move[0],move[1])
        self.next_turn(cost)
        self.set(move[0],move[1],0)
        for track in move:
            if(track not in self.player_nodes_in_reach[playerNum][0]):
                #Update distances for this track placement
                if(update):
                    for i in range(0,len(self.hubs)):
                        if(i==playerNum):
                            continue
                        hub=self.hubs[i]
                        if(self.distances_left[playerNum][hub]>0):
                            for compare_track in self.player_nodes_in_reach[i][0]:
                                if(costs[track[0]][track[1]][compare_track[0]][compare_track[1]]<self.distances_left[playerNum][hub]):
                                    self.distances_left[playerNum][hub]=costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
                                if(costs[track[0]][track[1]][compare_track[0]][compare_track[1]]<self.distances_left[i][self.hubs[playerNum]]):
                                    self.distances_left[i][self.hubs[playerNum]]=costs[track[0]][track[1]][compare_track[0]][compare_track[1]]
                    for city in self.cities.values():
                        for location in city.values():
                            if(costs[track[0]][track[1]][location[0]][location[1]]<self.distances_left[playerNum][location]):
                                self.distances_left[playerNum][location]=costs[track[0]][track[1]][location[0]][location[1]]
                    for i in range(0,len(self.hubs)):
                        for j in range(0,len(self.hubs)):
                            if(self.distances_left[j][self.hubs[playerNum]]+self.distances_left[playerNum][self.hubs[i]]<self.distances_left[j][self.hubs[i]]):
                                self.distances_left[j][self.hubs[i]]=self.distances_left[j][self.hubs[playerNum]]+self.distances_left[playerNum][self.hubs[i]]
                            if(self.distances_left[i][self.hubs[playerNum]]+self.distances_left[playerNum][self.hubs[j]]<self.distances_left[i][self.hubs[j]]):
                                self.distances_left[i][self.hubs[i]]=self.distances_left[i][self.hubs[playerNum]]+self.distances_left[playerNum][self.hubs[j]]
                        for city in self.cities.values():
                            for location in city.values():
                                if(self.distances_left[i][location]>self.distances_left[playerNum][location]+self.distances_left[i][self.hubs[playerNum]]):
                                    self.distances_left[i][location]=self.distances_left[playerNum][location]+self.distances_left[i][self.hubs[playerNum]]
                                if(self.distances_left[playerNum][location]>self.distances_left[i][location]+self.distances_left[playerNum][self.hubs[i]]):
                                    self.distances_left[playerNum][location]=self.distances_left[i][location]+self.distances_left[playerNum][self.hubs[i]]


                if track in self.player_nodes_in_reach[playerNum][cost]:
                    self.player_nodes_in_reach[playerNum][cost].remove(track)
                self.player_nodes_in_reach[playerNum][0].add(track)
                reachable=self.get_neighbors(track)
                for i in range(0,len(reachable)):
                    node=reachable[i][0]
                    worth=True
                    for j in range(0,reachable[i][1]):
                        if(node in self.player_nodes_in_reach[playerNum][j]):
                            worth=False
                            break
                    if(worth):
                        self.player_nodes_in_reach[playerNum][reachable[i][1]].add(node)
                for i in range(0,len(self.player_nodes_in_reach)):
                    if(i==playerNum):
                        continue
                    elif(track in self.player_nodes_in_reach[i][0]):
                        for j in range(0,3):
                            self.player_nodes_in_reach[playerNum][j].update(self.player_nodes_in_reach[i][j])
                            self.player_nodes_in_reach[i][j]=self.player_nodes_in_reach[playerNum][j]
        for i in range(0,len(self.player_nodes_in_reach)):
            if(i==playerNum):
                continue
            for track in move:
                if(track in self.player_nodes_in_reach[i][0]):
                    for j in range(0,3):
                        self.player_nodes_in_reach[playerNum][j].update(self.player_nodes_in_reach[i][j])
                        self.player_nodes_in_reach[i][j]=self.player_nodes_in_reach[playerNum][j]
                    self.player_nodes_in_reach[playerNum][2].difference_update(self.player_nodes_in_reach[playerNum][1])
                    self.player_nodes_in_reach[playerNum][2].difference_update(self.player_nodes_in_reach[playerNum][0])
                    self.player_nodes_in_reach[playerNum][1].difference_update(self.player_nodes_in_reach[playerNum][0])
        return True

    def unmake_move(self,root_board,move,playerNum):
        for track in move:
            self.set(track[0],track[1],root_board.cost(track[0],track[1]))
            self.turn=self.turn-1
            self.turn=self.turn%len(self.hubs)
        return True

    def check_winner(self,players,hands):
        totals=[]
        for i in range(0,len(self.hubs)):
            if(self.hubs[i]==None):
                totals.append(None)
                continue
            totals.append(0)
            tempcosts=self.computeCosts(self.hubs[i])
            for city in hands[players[i][0]].values():
                totals[i]+=tempcosts[city[0]][city[1]]
        for i in range(0,len(totals)):
            if(totals[i]==0):
                return i,totals
        return None,totals

    def next_turn(self,tracks):
        if(self.tracks_left-tracks==0):
            self.turn+=1
            self.turn=self.turn%len(self.hubs)
            self.tracks_left=2
        else:
            self.tracks_left=self.tracks_left-tracks

    def get_turn(self):
        return 2*self.turn-1

