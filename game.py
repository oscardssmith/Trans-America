import board
import mapFeatures
import random
import mcts

class game:
    board=None
    features=None
    players=[]
    hands={}

    def __init__(self,players,features):
        self.features=features

        self.players=players
        hubs=[]
        for player in self.players:
            self.hands[player[0]]={}
            hubs.append(player[2])
        self.board=board.grid(mapFeatures.mountains,mapFeatures.oceans,len(players),hubs)
        for key in self.features.cities.keys():
            values=[]
            for i in self.features.cities[key].keys():
                values.append(i)
            cities=random.sample(values,len(self.players))
            for i in range(0,len(self.players)):
                self.hands[players[i][0]][cities[i]]=self.features.cities[key][cities[i]]
    def make_move(self,player,move):
        return self.board.make_move(player,move)


g=game([["Bob",1,(0,0)],["bill",2,(0,0)],["a",3,None],["c",4,(0,0)],["d",5,(0,0)],["e",6,(0,0)],["f",7,(0,0)]],mapFeatures)
#print(g.graph.nodes)
#print(g.players[0][2])
print(g.board.check_winner(g.players,g.hands))
print(g.board.computeCosts((0,0)))
for player in g.players:
    print(g.board.get_moves(player[2]))
print(g.board.make_move(0,[((0,0),(1,0))] ))
print(g.board.check_winner(g.players,g.hands))
#print(g.board.check_winner(board.make_move(g.graph,g.players[0],(1,0))[0],g.players,g.hands))
#g.check_winner(g.graph)
#print(g.hands)
