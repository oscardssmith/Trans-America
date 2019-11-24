import mapFeatures
import networkx as nx


def makeGraph(grid):
    boardGraph=nx.Graph()
    for i in range(0,len(grid.board)):
        for j in range(0,len(grid.board[0])):
            neighbors=grid.get_neighbors((i,j))
            for neighbor in neighbors:
                boardGraph.add_edge((i,j),neighbor[0],weight=neighbor[1])
    return boardGraph

def check_winner(graph,players,hands):
    totals=[]
    for i in range(0,len(players)):
        if(players[i][2]==None):
            totals.append(None)
            continue
        else:
            totals.append(0)
        for city in hands[players[i][0]].values():
            totals[i]+=nx.shortest_path_length(graph,players[i][2],city)
    for i in range(0,len(totals)):
        if(totals[i]==0):
            return i,totals
    #print(nx.to_dict_of_dicts(graph))
    return False,totals

def get_moves(graph,player):
    if(player[2]!=None):
        return graph[player[2]]
    else:
        return graph.nodes

def get_turn():
    return None

def make_move(graph,player,node):
    if(player[2]==None):
        player[2]=node
        return graph,player
    else:
        return nx.contracted_nodes(graph, player[2],node,False),player

class grid:
    board=[]
    costs=[]
    def __init__(self, mountains, oceans):
        for i in range(0,13):
            self.board.append([])
            for j in range(0,20):
                #print(i,j)
                self.board[i].append([[0,1],[1,1]])

        #print(self.board)
        for mountain in mountains:
            #print(mountain)
            self.set(mountain[0],mountain[1],2)
        for ocean in oceans:
            #print(ocean)
            for neighbor in self.get_neighbors(ocean):
                #print(neighbor)
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
        
    def computeCosts(self,point):
        out=[]
        for i in range(0,self.size()[0]):
            temp=[]
            for j in range(0,self.size()[1]):
                temp.append(2*self.size()[0]*self.size()[1])
            out.append(temp)
        toCheck=[]
        out[point[0]][point[1]]=0
        toCheck.append(point)
        while(not len(toCheck)==0):
            test=toCheck.pop(0)
            for neighbor in self.get_neighbors(test):
                if(out[test[0]][test[1]]+neighbor[1]<out[neighbor[0][0]][neighbor[0][1]]):
                    out[neighbor[0][0]][neighbor[0][1]]=out[test[0]][test[1]]+neighbor[1]
                    toCheck.append(neighbor[0])
        #print(out)
        return out

        
