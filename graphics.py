import pygame
import pygame.gfxdraw
import board
import mapFeatures
import math
from math import cos, sin


colors={'blue':(128,128,255),
    'green':(0,196,0),
    'red':(200,0,0),
    'orange':(200,128,0),
    'yellow':(210,210,0)
}

xres = 1600
yres = 900
show_real = True
class window:
    '''draws everything'''
    screen = None
    cities = None
    s=None
    font=None
    basis=None
    extrema=None
    scaling=None
    def __init__(self,width,height,features,basis = ([1,0],[-0.5,math.sqrt(3)/4])):
        pygame.init()
        self.font=pygame.font.SysFont(None, 24)
        self.screen=pygame.display.set_mode((width,height))
        self.s=pygame.Surface((xres,yres))
        self.basis=basis
        self.cities=features.cities
        temp=features.corners
        self.extrema=((temp[1][1]*self.basis[0][0]+temp[1][0]*self.basis[1][0],temp[1][1]*self.basis[0][1]+temp[1][0]*self.basis[1][1]),
         (temp[0][1]*self.basis[0][0]+temp[0][0]*self.basis[1][0],temp[0][1]*self.basis[0][1]+temp[0][0]*self.basis[1][1]))
        self.scaling=(self.s.get_size()[0]/abs(self.extrema[0][0]-self.extrema[1][0]),self.s.get_size()[1]/abs(self.extrema[0][1]-self.extrema[1][1]))
    
    
    def get_coords(self,i,j):
        '''board coords to screen coords'''
        i += 1
        j += 1
        if show_real:
            # Don't show the 'human scale' version of the board; represent it
            #  as the computer sees it
            return (j * 70, i * 60)
        else:
            return (int(self.scaling[0]*(j*self.basis[0][0]+i*self.basis[1][0]-self.extrema[1][0])),
                    int(self.scaling[1]*(j*self.basis[0][1]+i*self.basis[1][1])))
                
    def draw(self,board, hands):
        # Draw the lines
        for i in range(0,board.size()[0]):
            for j in range(0,board.size()[1]):
                for point in board.get_neighbors((i,j),0,2):
                    #print(point)
                    p1 = self.get_coords(point[0][0], point[0][1])
                    p2 = self.get_coords(i,j)
                    color=(128,128,128)
                    if(point[1]==0):
                        color=(255,255,255)
                    self.draw_thicc_line(p1, p2, abs(7*point[1]-6),color)
                    
        # Draw cities
        for color in self.cities.keys():
            for city in self.cities[color].values():
                center = self.get_coords(city[0],city[1])
                pygame.gfxdraw.aacircle(self.s, center[0], center[1], int(0.25*min(self.scaling)), colors[color])
                pygame.gfxdraw.filled_circle(self.s, center[0], center[1], int(0.25*min(self.scaling)), colors[color])
        
        
        # Draw player cities
        player_colors = ((255,255,255), (0,0,0))
        for player, hand in hands.items():
            for city in hand.values():
                pygame.draw.circle(self.s,player_colors[player],
                                    self.get_coords(city[0],city[1]),
                                    int(0.2*min(self.scaling)),
                                    2)
        # draw hubs if placed
        for player, hub in enumerate(board.hubs):
            if hub is None:
                continue
            pygame.draw.circle(self.s,player_colors[player],
                                self.get_coords(hub[0],hub[1]),
                                int(0.1*min(self.scaling)))
        #pygame.draw.line(s,(255,255,255),(50,0),(50,100))
        self.screen.blit(self.s,(0,0))
        pygame.display.update()
    
    def draw_thicc_line(self, p0, p1, thickness, color = (255,255,255)):
        ''' utility function to draw anti-aliased thcik lines. '''
        center_x = (p0[0]+p1[0])/2
        center_y = (p0[1]+p1[1])/2
        # The +1 is to get out of the domain error
        angle = math.atan2(p0[1]-p1[1]+1,
                           p0[0]-p1[0])
        
        
        hlength = math.hypot(p0[0]-p1[0], p0[1]-p1[1])/2. - 2
        hthick = thickness/2.
        sangle = math.sin(angle)
        cangle = math.cos(angle)
        UL = (center_x + hlength*cangle - hthick *sangle,
              center_y + hthick *cangle + hlength*sangle)
        UR = (center_x - hlength*cangle - hthick *sangle,
              center_y + hthick *cangle - hlength*sangle)
        BL = (center_x + hlength*cangle + hthick *sangle,
              center_y - hthick *cangle + hlength*sangle)
        BR = (center_x - hlength*cangle + hthick *sangle,
              center_y - hthick *cangle - hlength*sangle)
        pygame.gfxdraw.aapolygon(self.s, (UL, UR, BR, BL), color)
        #if not a double cost location, fill in the line
        if thickness != 8:
            pygame.gfxdraw.filled_polygon(self.s, (UL, UR, BR, BL), color)
        

    def draw_text(self, box, hoffset):
        sz = box.get_size()
        dest = pygame.Rect(xres - sz[0], yres - sz[1] - hoffset, sz[0], sz[1])
        self.screen.blit(box, dest)
        pygame.display.update()

    def draw_turn(self, turn, player, tracks):
        turnbox = self.font.render("Turn {} ".format(turn), True, (255, 255, 255))
        playerbox = self.font.render("Player {} ".format(player), True, (255, 255, 255))
        trackbox = self.font.render("Tracks Left {} ".format(tracks), True, (255, 255, 255))
        maxw = turnbox.get_size()[0]
        h = turnbox.get_size()[1] + 3
        if playerbox.get_size()[0] > maxw:
            maxw = playerbox.get_size()[0]
        if trackbox.get_size()[0] > maxw:
            maxw = trackbox.get_size()[0]

        # Clear a more than large enough space
        dest = pygame.Rect(xres - maxw * 2, yres - h * 3, maxw * 2, h * 3)
        self.s.fill((0, 0, 0), dest)

        self.draw_text(turnbox, 0)
        self.draw_text(playerbox, h)
        self.draw_text(trackbox, h * 2)

