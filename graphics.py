import pygame
import board
import TAmap
import minTotalAI
import math

colors={'blue':(128,128,255),
    'green':(0,196,0),
    'red':(200,0,0),
    'orange':(200,128,0),
    'yellow':(210,210,0)
}

pygame.init()
screen = pygame.display.set_mode((1280,640))
s=pygame.Surface((1280,640))

basis=([1,0],[-0.5,math.sqrt(3)/4])

testgrid=board.grid(TAmap.mountains,TAmap.oceans)

temp=((12,5),(0,16))

extrema=((testgrid.size()[1]*basis[0][0],testgrid.size()[1]*basis[0][1]),(testgrid.size()[0]*basis[1][0],testgrid.size()[0]*basis[1][1]))
extrema=((temp[1][1]*basis[0][0]+temp[1][0]*basis[1][0],temp[1][1]*basis[0][1]+temp[1][0]*basis[1][1]),
         (temp[0][1]*basis[0][0]+temp[0][0]*basis[1][0],temp[0][1]*basis[0][1]+temp[0][0]*basis[1][1]))


p1=minTotalAI.minTotalAI(testgrid,TAmap.cities)
scaling=(s.get_size()[0]/abs(extrema[0][0]-extrema[1][0]),s.get_size()[1]/abs(extrema[0][1]-extrema[1][1]))
#print(extrema)
#print(scaling)

def get_coords(i,j,extrema,scaling):
    return (int(scaling[0]*(j*basis[0][0]+i*basis[1][0]-extrema[1][0])),int(scaling[1]*(j*basis[0][1]+i*basis[1][1])))
    
print(get_coords(0,19,extrema,scaling))
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
    for i in range(0,testgrid.size()[0]):
        for j in range(0,testgrid.size()[1]):
            for point in testgrid.get_neighbors((i,j)):
                #print(point)
                pygame.draw.line(s,(255,255,255),get_coords(point[0][0],point[0][1],extrema,scaling),get_coords(i,j,extrema,scaling),7*point[1]-6)
    #print(board.cities.keys())
    for color in TAmap.cities.keys():
        for city in TAmap.cities[color].values():
            pygame.draw.circle(s,colors[color],get_coords(city[0],city[1],extrema,scaling),int(0.25*min(scaling)))
    pygame.draw.circle(s,(255,255,255),get_coords(p1.hub[0],p1.hub[1],extrema,scaling),int(0.25*min(scaling)))
    #pygame.draw.line(s,(255,255,255),(50,0),(50,100))
    screen.blit(s,(0,0))
    pygame.display.update()
