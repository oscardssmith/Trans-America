""" window.py provides graphical drawing support """
import math
import pygame
import pygame.gfxdraw
import features

WHITE = (255, 255, 255)

COLORS = {
    'blue': (128, 128, 255),
    'green': (0, 196, 0),
    'red': (200, 0, 0),
    'orange': (200, 128, 0),
    'yellow': (210, 210, 0)
}

PLAYER_COLORS = (
    (128, 128, 255),
    (0, 196, 0),
    (200, 0, 0),
    (210, 210, 0),
    (255, 255, 255),
    (150, 75, 0),
)

class Window:
    '''draws everything'''
    screen = None
    cities = None
    surface = None
    font = None
    basis = None
    extrema = None
    scaling = None
    scaled = False
    def __init__(self, width, height, scaled=False, basis=([1, 0], [-0.5, math.sqrt(3)/4])):
        pygame.init()
        self.font = pygame.font.SysFont(None, 24)
        self.width = width
        self.height = height
        self.scaled = scaled
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))
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
            return (j * int(self.width / (features.LAST_COLUMN + 1)),
                    i * int((self.height - 50) / (features.LAST_ROW + 1)))

        return (int(self.scaling[0] * (j * self.basis[0][0] + i * self.basis[1][0] - self.extrema[1][0])), # pylint: disable=C0301
                int(self.scaling[1] * (j * self.basis[0][1] + i * self.basis[1][1])))

    def draw_lines(self, board):
        """ Draw the lines """
        for i in range(0, board.rows):
            for j in range(0, board.cols):
                for point in board.get_neighbors((i, j), 1, 2):
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
                radius = int(0.25 * min(self.scaling))
                pygame.gfxdraw.aacircle(self.surface, center[0], center[1], radius, COLORS[color])
                pygame.gfxdraw.filled_circle(self.surface, center[0], center[1], radius,
                                             COLORS[color])

    def draw_player_cities(self, hands):
        """ Draw the player cities """
        for player, hand in enumerate(hands):
            for city in hand.values():
                radius = int(0.25 * min(self.scaling))
                center = self.get_coords(city[0], city[1])
                pygame.draw.circle(self.surface, WHITE, center, radius, 2)
                box = pygame.Rect(center[0] - radius, center[1] - 1, radius * 2, 3)
                pygame.gfxdraw.box(self.surface, box, PLAYER_COLORS[player])

    def draw_hubs(self, hubs):
        """ draw hubs if placed """
        for player, hub in enumerate(hubs):
            if hub is None:
                continue
            radius = int(0.15 * min(self.scaling))
            center = self.get_coords(hub[0], hub[1])
            pygame.gfxdraw.aacircle(self.surface, center[0], center[1], radius + 1, WHITE)
            pygame.draw.circle(self.surface, PLAYER_COLORS[player], center, radius)
            #pygame.gfxdraw.line(self.surface, center[0] - radius, center[1] - radius,
            #                    center[0] + radius, center[1] + radius, WHITE)

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

        #  For some reason, drawing this twice seems to fill in lines better
        pygame.gfxdraw.aapolygon(self.surface, (upl, upr, btr, btl), color)
        pygame.gfxdraw.aapolygon(self.surface, (upl, upr, btr, btl), color)

        #if not a double cost location, fill in the line
        if thickness != 8:
            pygame.gfxdraw.filled_polygon(self.surface, (upl, upr, btr, btl), color)

    def draw_move(self, move):
        """ Draw one move """
        point1 = self.get_coords(move[0][0], move[0][1])
        point2 = self.get_coords(move[1][0], move[1][1])
        self.draw_thicc_line(point1, point2, 6)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def draw_text(self, box, hoffset):
        """ Draw text onto our surface """
        size = box.get_size()
        dest = pygame.Rect(self.width - size[0], self.height - size[1] - hoffset, size[0], size[1])
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
        dest = pygame.Rect(self.width - maxw * 2, self.height - h * 3, maxw * 2, h * 3)
        self.surface.fill((0, 0, 0), dest)

        self.draw_text(turnbox, 0)
        self.draw_text(playerbox, h)
        self.draw_text(trackbox, h * 2)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def draw_standings(self, standings):
        """ Draw the standings """
        left = 3
        for i, distance in enumerate(standings):
            box = self.font.render("Player {0:1}: {1:4}".format(i + 1, distance), True,
                                   PLAYER_COLORS[i])
            top = self.height - box.get_size()[1] - 3
            if left == 3:
                dest = pygame.Rect(left, top, 6 * (box.get_size()[0] + 15), box.get_size()[1])
                self.surface.fill((0, 0, 0), dest)
            self.surface.blit(box, (left, top))
            self.screen.blit(self.surface, (0, 0))
            pygame.display.update()
            left += box.get_size()[0] + 10


    def clear(self):
        """ Clear the whole board """
        dest = pygame.Rect(0, 0, self.width, self.height)
        self.surface.fill((0, 0, 0), dest)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def draw_initial(self, board, hands):
        """ Draw the whole board """
        self.draw_lines(board)
        self.draw_cities()
        self.draw_player_cities(hands)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()
