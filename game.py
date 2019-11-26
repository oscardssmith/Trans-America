import board
import mapFeatures
import random
import mcts
import minTotalAI
import minDifferenceAI
import copy
import graphics
import pygame

class game:
    ''' class for runnign a single game. '''
    features=None

    def __init__(self,players,features, inboard=None,hands=None):
        self.features=features
        self.hands={}
        self.board=None
        self.players=players
        hubs=[]
        for player in self.players:
            self.hands[player[0]]={}
            if(len(player)>2):
                hubs.append(player[2])
        if(inboard==None):
            self.board=board.grid(mapFeatures,len(players),hubs)
        else:
            self.board=inboard
        for key in self.features.cities.keys():
            values=[]
            for i in self.features.cities[key].keys():
                values.append(i)
            cities=random.sample(values,len(self.players))
            for i in range(0,len(self.players)):
                self.hands[players[i][0]][cities[i]]=self.features.cities[key][cities[i]]
        for i in range(0,len(self.players)):
            self.players[i][1]=self.players[i][1].init(copy.deepcopy(self.board),self.features,self.players[i][0],self.hands)
    
    def take_turn(self):
        move=self.players[self.board.turn][1].move(copy.deepcopy(self.board))
        self.board.make_move(move, self.board.turn)
        return self.board.is_terminal(self.hands)
        
    def make_move(self, move, player):
        return self.board.make_move(move, player)

    def play_game(self):
        while not self.board.is_terminal(self.hands):
            self.take_turn()
        return self.board.value(self.hands)

def run_tournament(num, ai1, ai2):
    wins=[0,0,0]
    while(sum(wins)<num):
        players = [[0,ai1],[1,ai2]]
        g = game(players,mapFeatures)

        gBoard = copy.deepcopy(g.board)
        hands2 = copy.deepcopy(g.hands)
        winner1 = g.play_game()

        g2 = game([[0,ai2],[1,ai1]],mapFeatures,gBoard,hands2)
        winner2 =g2.play_game()
        if winner1 != winner2:
            print(winner1)
            wins[winner1]+=1
        else:
            print("draw")
            wins[2]+=1
    print(wins)

def run_graphics(ai1, ai2):
    players=[[0,ai1],[1,ai2]]
    g=game(players,mapFeatures)
    
    w = graphics.window(graphics.xres,graphics.yres,mapFeatures)
    grid=g.board

    running = True
    done = False
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not done:
                    done=g.take_turn()
                    if done:
                        print(g.board.value(g.hands))
                if event.key == pygame.K_q:
                    running = False
        w.draw(g.board, g.hands)

if __name__ == '__main__':
    run_graphics(mcts, minDifferenceAI)
    #run_graphics(minTotalAI, minDifferenceAI)
    #run_tournament(100, mcts, minDifferenceAI)
