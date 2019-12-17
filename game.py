#!/usr/bin/python3
import board
import random
import copy
import graphics

class Game:
    ''' class for running a single game. '''
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
            self.board=board.grid(features,len(players),hubs)
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
