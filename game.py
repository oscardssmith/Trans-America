import board
import mapFeatures
import networkx as nx
import random

class game:
    board=None
    features=None
    players=[]
    hands={}
    graph=None

    def __init__(self,players,features):
        self.features=features
        self.board=board.grid(mapFeatures.mountains,mapFeatures.oceans)
        self.graph=board.makeGraph(self.board)
        self.players=players
        for player in self.players:
            self.hands[player[0]]={}
        for key in self.features.cities.keys():
            values=[]
            for i in self.features.cities[key].keys():
                values.append(i)
            cities=random.sample(values,len(self.players))
            for i in range(0,len(self.players)):
                self.hands[players[i][0]][cities[i]]=self.features.cities[key][cities[i]]


g=game([["Bob",1,(0,0)],["bill",2,(0,0)],["a",3,None],["c",4,(0,0)],["d",5,(0,0)],["e",6,(0,0)],["f",7,(0,0)]],mapFeatures)
print(g.graph.nodes)
print(g.players[0][2])
print(board.check_winner(g.graph,g.players,g.hands))
for player in g.players:
    print(board.get_moves(g.graph,player))
#g.check_winner(g.graph)
#print(g.hands)
