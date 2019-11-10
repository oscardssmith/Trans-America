cities = {'green':  {'Seatle': (0,0),
                     'Portland': (1,1),
                     'Medford': (3,1),
                     'Sacramento': (5,2),
                     'San Fransisco': (6,2),
                     'Los Angeles': (9,5),
                     'San Diego': (10,6)},
          'blue':   {'Helena': (1,3),
                     'Bismark': (1,7),
                     'Duluth': (1,10),
                     'Mineapolis': (2,10),
                     'Buffalo': (2,15),
                     'Chicago': (3,13),
                     'Cincinati': (5,15)},
          'orange': {'Boston': (2,17),
                     'New York City': (4,17),
                     'Washington': (5,17),
                     'Richmond': (7,18),
                     'Winston': (8,17),
                     'Jacksonville': (12,19),
                     'Charleston': (10,19)},
          'yellow': {'Salt Lake City': (4,4),
                     'Omaha': (4,9),
                     'Denver': (5,7),
                     'Kansas': (6,11),
                     'St. Louis': (6,13),
                     'Santa Fe': (8,8),
                     'Oklahoma City': (8,11)},
          'red':    {'Phoenix': (9,5),
                     'El Paso': (11,8),
                     'Memphis': (9,15),
                     'Dallas': (10,13),
                     'Atlanta': (10,17),
                     'Houston': (12,14),
                     'New Orleans': (12,16)}}

class grid:
    board=[]
    def __init__(self):
        for i in range(0,13):
            self.board.append([])
            for j in range(0,20):
                print(i,j)
                self.board[i].append([[0,1],[1,1]])

        print(self.board)

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
