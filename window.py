""" window.py provides graphical drawing support """
import math
import pygame
import pygame.gfxdraw
import features


COLORS = {
    'blue': (128, 128, 255),
    'green': (0, 196, 0),
    'red': (200, 0, 0),
    'orange': (200, 128, 0),
    'yellow': (210, 210, 0)
}
PLAYER_COLORS = ((255, 255, 255), (0, 0, 0))

XRES = 1600
YRES = 900
class Window:
    '''draws everything'''
    screen = None
    cities = None
    s = None
    font = None
    basis = None
    extrema = None
    scaling = None
    scaled = False
    def __init__(self, basis=([1, 0], [-0.5, math.sqrt(3)/4])):
        pygame.init()
        self.font = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode((XRES, YRES))
        self.surface = pygame.Surface((XRES, YRES))
        self.basis = basis
        self.cities = features.CITIES
        temp = features.CORNERS
        self.extrema = ((temp[1][1]*self.basis[0][0]+temp[1][0]*self.basis[1][0],
                         temp[1][1]*self.basis[0][1]+temp[1][0]*self.basis[1][1]),
                        (temp[0][1]*self.basis[0][0]+temp[0][0]*self.basis[1][0],
                         temp[0][1]*self.basis[0][1]+temp[0][0]*self.basis[1][1]))
        self.scaling = (self.surface.get_size()[0] / abs(self.extrema[0][0] - self.extrema[1][0]),
                        self.surface.get_size()[1] / abs(self.extrema[0][1] - self.extrema[1][1]))


    def get_coords(self, i, j):
        '''board coords to screen coords'''
        i += 1
        j += 1
        if not self.scaled:
            # Don't show the 'human scale' version of the board; represent it
            #  as the computer sees it
            return (j * 70, i * 60)

        return (int(self.scaling[0] * (j * self.basis[0][0] + i * self.basis[1][0] - self.extrema[1][0])), # pylint: disable=C0301
                int(self.scaling[1] * (j * self.basis[0][1] + i * self.basis[1][1])))

    def draw_lines(self, board):
        """ Draw the lines """
        for i in range(0, board.size()[0]):
            for j in range(0, board.size()[1]):
                for point in board.get_neighbors((i, j), 0, 2):
                    point1 = self.get_coords(point[0][0], point[0][1])
                    point2 = self.get_coords(i, j)
                    color = (128, 128, 128)
                    if point[1] == 0:
                        color = (255, 255, 255)
                    self.draw_thicc_line(point1, point2, abs(7*point[1]-6), color)

    def draw_cities(self):
        """ Draw the cities """
        for color, citygroup in self.cities.items():
            for city in citygroup.values():
                center = self.get_coords(city[0], city[1])
                pygame.gfxdraw.aacircle(self.surface, center[0], center[1],
                                        int(0.25*min(self.scaling)), COLORS[color])
                pygame.gfxdraw.filled_circle(self.surface, center[0], center[1],
                                             int(0.25*min(self.scaling)), COLORS[color])

    def draw_player_cities(self, hands):
        """ Draw the player cities """
        for player, hand in hands.items():
            for city in hand.values():
                pygame.draw.circle(self.surface, PLAYER_COLORS[player],
                                   self.get_coords(city[0], city[1]),
                                   int(0.2 * min(self.scaling)), 2)

    def draw_hubs(self, board):
        """ draw hubs if placed """
        for player, hub in enumerate(board.hubs):
            if hub is None:
                continue
            pygame.draw.circle(self.surface, PLAYER_COLORS[player],
                               self.get_coords(hub[0], hub[1]),
                               int(0.1 * min(self.scaling)))

    def draw_thicc_line(self, point0, point1, thickness, color=(255, 255, 255)):
        ''' utility function to draw anti-aliased thick lines. '''
        center_x = (point0[0] + point1[0]) / 2
        center_y = (point0[1] + point1[1]) / 2
        # The +1 is to get out of the domain error
        angle = math.atan2(point0[1] - point1[1] + 1,
                           point0[0] - point1[0])


        hlength = math.hypot(point0[0] - point1[0], point0[1] - point1[1]) / 2. - 2
        hthick = thickness / 2.
        sangle = math.sin(angle)
        cangle = math.cos(angle)
        upl = (center_x + hlength*cangle - hthick *sangle,
               center_y + hthick *cangle + hlength*sangle)
        upr = (center_x - hlength*cangle - hthick *sangle,
               center_y + hthick *cangle - hlength*sangle)
        btl = (center_x + hlength*cangle + hthick *sangle,
               center_y - hthick *cangle + hlength*sangle)
        btr = (center_x - hlength*cangle + hthick *sangle,
               center_y - hthick *cangle - hlength*sangle)
        pygame.gfxdraw.aapolygon(self.surface, (upl, upr, btr, btl), color)
        #if not a double cost location, fill in the line
        if thickness != 8:
            pygame.gfxdraw.filled_polygon(self.surface, (upl, upr, btr, btl), color)


    def draw_text(self, box, hoffset):
        """ Draw text onto our surface """
        size = box.get_size()
        dest = pygame.Rect(XRES - size[0], YRES - size[1] - hoffset, size[0], size[1])
        self.surface.blit(box, dest)

    def draw_turn(self, turn, player, tracks):
        """ Draw text boxes describing the turn """
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
        dest = pygame.Rect(XRES - maxw * 2, YRES - h * 3, maxw * 2, h * 3)
        self.surface.fill((0, 0, 0), dest)

        self.draw_text(turnbox, 0)
        self.draw_text(playerbox, h)
        self.draw_text(trackbox, h * 2)

        pygame.display.update()

    def draw(self, board, hands):
        """ Draw the whole board """
        self.draw_lines(board)
        self.draw_cities()
        self.draw_player_cities(hands)
        self.draw_hubs(board)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()
