import mapFeatures
import queue

class grid:
    def __init__(self, mountains, oceans,numPlayers,hubs=[]):
        self.turn=0
        self.board=[]
        self.costs=[]
        self.hubs=[]
        if(len(hubs)==0):
            for i in range(0,numPlayers):
                self.hubs.append(None)
        else:
            self.hubs=hubs
        for i in range(0,13):
            self.board.append([])
            for j in range(0,20):
                self.board[i].append([[0,1],[1,1]])

        for mountain in mountains:
            self.set(mountain[0],mountain[1],2)
        for ocean in oceans:
            for neighbor in self.get_neighbors(ocean):
                self.set(ocean,neighbor[0],3)
        for i in range(0,13):
            self.costs.append([])
            for j in range(0,20):
                self.costs[i].append(self.computeCosts((i,j)))


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
        moves = set()
        if(hub==None):
            for i in range(0,self.size()[0]):
                for j in range(0,self.size()[1]):
                    if(len(self.get_neighbors((i,j)))!=0):
                        moves.add((i,j))
            return moves
        visited=self.LCS(hub,2)
        pareddown=[{},{},{}]
        for point in visited[2].keys():
            if(visited[2][point] in visited[0] or visited[2][point] in visited[1]):
                pareddown[2][point]=visited[2][point]
        for point in visited[1].keys():
            if(visited[1][point] in visited[0]):
                pareddown[1][point]=visited[1][point]
        for point in visited[0].keys():
            pareddown[0][point]=visited[0][point]
        for point in pareddown[2].keys():
            if(pareddown[2][point] in pareddown[0]):
                moves.add(((point,pareddown[2][point]), ))
            else:
                secondMove=pareddown[2][point]
                while(secondMove not in pareddown[1]):
                    secondMove=visited[1][secondMove]
                
                moves.add(((point,pareddown[2][point]),(pareddown[1][secondMove],secondMove)))
        temp=list(pareddown[1].keys())
        for i in range(1,len(temp)):
            for j in range(0,i-1):
                moves.add(((temp[i],pareddown[1][temp[i]]),(pareddown[1][temp[j]],temp[j])))
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
        

    def LCS(self,point,cutoff):
        visited=[]
        for i in range(0,cutoff+1):
            visited.append({})
        toCheck=queue.PriorityQueue()
        toCheck.put((0,(point,None)))
        visited[0][point]=None
        while(not toCheck.empty()):
            value,track=toCheck.get()
            test=track[0]
            for neighbor in self.get_neighbors(test,0,2):
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
    
    def is_terminal(self, hands):
        for player in hands.values():
            player_done = True
            for city in player.values():
                if len(self.get_neighbors(city,0,0)) == 0:
                    player_done = False
                    break
            if player_done:
                for city in player.values():
                    visited = self.LCS(city,0)[0]
                    for city in player.values():
                        if city not in visited:
                            player_done = False
                    break
            if player_done:
                return True
        return False
        
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

    def make_move(self,move,playerNum):
        if(self.turn!=playerNum):
            return False
        if(self.hubs[playerNum]==None):
            self.hubs[playerNum]=move
        else:
            for track in move:
                self.set(track[0],track[1],0)
        self.next_turn()
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

    def next_turn(self):
        self.turn+=1
        self.turn=self.turn%len(self.hubs)

    def get_turn(self):
        return 2*self.turn-1

