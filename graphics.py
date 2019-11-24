import pygame
import board
import mapFeatures
import minTotalAI
import math
import networkx as nx

colors={'blue':(128,128,255),
    'green':(0,196,0),
    'red':(200,0,0),
    'orange':(200,128,0),
    'yellow':(210,210,0)
}

class window:
    screen = None
    cities = None
    s=None
    basis=None
    extrema=None
    scaling=None
    def __init__(self,width,height,features,basis = ([1,0],[-0.5,math.sqrt(3)/4])):
        pygame.init()
        self.screen=pygame.display.set_mode((width,height))
        self.s=pygame.Surface((1280,640))
        self.basis=basis
        self.cities=features.cities
        temp=features.corners
        self.extrema=((temp[1][1]*self.basis[0][0]+temp[1][0]*self.basis[1][0],temp[1][1]*self.basis[0][1]+temp[1][0]*self.basis[1][1]),
         (temp[0][1]*self.basis[0][0]+temp[0][0]*self.basis[1][0],temp[0][1]*self.basis[0][1]+temp[0][0]*self.basis[1][1]))
        self.scaling=(self.s.get_size()[0]/abs(self.extrema[0][0]-self.extrema[1][0]),self.s.get_size()[1]/abs(self.extrema[0][1]-self.extrema[1][1]))
    
    
    def get_coords(self,i,j):
        i += 1
        j += 1
        return (int(self.scaling[0]*(j*self.basis[0][0]+i*self.basis[1][0]-self.extrema[1][0])),
            int(self.scaling[1]*(j*self.basis[0][1]+i*self.basis[1][1])))
    def draw(self,board):
        for i in range(0,board.size()[0]):
            for j in range(0,board.size()[1]):
                for point in board.get_neighbors((i,j)):
                    #print(point)
                    pygame.draw.line(self.s,(255,255,255),self.get_coords(point[0][0],point[0][1]),self.get_coords(i,j),7*point[1]-6)
        #print(board.cities.keys())
        for color in self.cities.keys():
            for city in self.cities[color].values():
                pygame.draw.circle(self.s,colors[color],self.get_coords(city[0],city[1]),int(0.25*min(self.scaling)))
        #pygame.draw.circle(self.s,(255,255,255),get_coords(p1.hub[0],p1.hub[1],extrema,scaling),int(0.25*min(scaling)))
        #pygame.draw.line(s,(255,255,255),(50,0),(50,100))
        self.screen.blit(self.s,(0,0))
        pygame.display.update()


w = window(1280,640,mapFeatures)
grid=board.grid(mapFeatures.mountains,mapFeatures.oceans)
p1=minTotalAI.minTotalAI(grid,mapFeatures.cities)
graph=board.makeGraph(grid)

#print(nx.to_dict_of_dicts(graph))

def get_coords(i,j,extrema,scaling):
    i += 1
    j += 1
    return (int(scaling[0]*(j*basis[0][0]+i*basis[1][0]-extrema[1][0])),
            int(scaling[1]*(j*basis[0][1]+i*basis[1][1])))
    
#print(get_coords(0,19,extrema,scaling))
running = True
#print(testgrid.costs)
    # main loop
while running:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
    w.draw(grid)
