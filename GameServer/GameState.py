from GameBoard import GameBoard
from PlayerState import PlayerState

class GameState(object):
    def __init__(self, nplayers):
        self.board = GameBoard()
        self.players = [PlayerState(i) for i in range(0, nplayers)]
        self.longestroad = None
        self.largestarmy = None
        self.turn = 0
        self.phase = None
        self.progress = 'going'
        self.lastroll = None

    def accept(self, v):
        v.visit(self)
        for p in self.players:
            p.accept(v)
        self.board.accept(v)

    def addResource(self, player, resource, amount):
        self.players[player].addResource(resource, amount)
    def removeResource(self, player, resource, amount):
        self.players[player].removeResource(resource, amount)

    def addCard(self, player, card):
        self.players[player].addCard(card)
    def removeCard(self, player, card):
        self.players[player].removeCard(card)

    def updateScore(self, player):
        c = self.board.getCount(player, 'city')
        s = self.board.getCount(player, 'settlement')
        army = 2 if (player == self.largestarmy) else 0
        road = 2 if (player == self.longestroad) else 0
        vpcards = self.player.cards[vp]
        self.players[player].score = c*2 + s + army + road

    def addBuilding(self, player, building, corner):
        self.board.addBuilding(corner, player, building)
    def addRoad(self, a, b, player):
        self.board.addRoad(a,b,player)

    def updateRemaining(self, player):
        c = self.board.getCount(player, 'city')
        startingCities = self.players[player].startingBuildings["city"]
        r = self.board.getCount(player, 'road')
        startingRoads = self.players[player].startingBuildings["road"]
        s = self.board.getCount(player, 'settlement')
        startingSettlement = self.players[player].startingBuildings["settlement"]
        self.players[player].remBuildings["city"] = startingCities - c
        self.players[player].remBuildings["road"] = startingRoads - r
        self.players[player].remBuildings["settlement"] = startingSettlement - s

    def getRobber(self):
        return self.board.getRobber()
