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
    def check_winner(self,graph):
        for player in self.players:
            for coords in self.hands[player[0]].values():
                print(coords)
                graph.
        #print(nx.to_dict_of_dicts(graph))
        return False

g=game([["Bob",1],["bill",2],["a",3],["c",4],["d",5],["e",6],["f",7]],mapFeatures)
g.check_winner(g.graph)
print(g.hands)
