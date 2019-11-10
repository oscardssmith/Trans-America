import pygame
import board
import math

pygame.init()
screen = pygame.display.set_mode((1280,960))
s=pygame.Surface((1280,960))

basis=([1,0],[-0.5,math.sqrt(3)/4])

testgrid=board.grid()
extrema=((testgrid.size()[0]*basis[0][0],testgrid.size()[0]*basis[0][1]),(testgrid.size()[1]*basis[1][0],testgrid.size()[1]*basis[1][1]))
scaling=(s.get_size()[0]/abs(extrema[0][0]-extrema[1][0]),s.get_size()[1]/abs(extrema[0][1]-extrema[1][1]))
print(extrema)
print(scaling)
testgrid.set((4,5),(5,6),2)

def get_coords(i,j,extrema,scaling):
    return (int(scaling[0]*(i*basis[0][0]+j*basis[1][0]-extrema[1][0])),int(scaling[1]*(i*basis[0][1]+j*basis[1][1])))
    
print(get_coords(0,19,extrema,scaling))
running = True
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
            #pygame.draw.circle(s,(255,255,255),get_coords(i,j,extrema,scaling),int(0.1*min(scaling)))
    
    pygame.draw.line(s,(255,255,255),(0,0),(100,100))
    screen.blit(s,(0,0))
    pygame.display.update()
