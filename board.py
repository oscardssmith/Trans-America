

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


