from GameBoard import GameBoard
from PlayerState import PlayerState

class GameState(object):
    def __init__(self, players):
        self.board = GameBoard()
        self.players = [PlayerState(i) for i in range(0, players)]
        self.longestroad = None #int - PlayerId
        self.largestarmy = None #int - PlayerId
        self.turn = None #int - PlayerId
        #Phases: discard, buildsettle, buildroad, moverobber, respondtrade, chooseplayer, standard, ended, turnended
        self.phase = None
        self.phaseinfo = None
        self.lastroll = None #int - Roll value
        self.numturns = 0

    def accept(self, v):
        v.visit(self)
        for p in self.players:
            p.accept(v)
        self.board.accept(v)
    def maxPlayerScore(self):
        return max([player.score for player in self.players])
    def addResource(self, player, resource, amount):
        self.players[player].addResource(resource, amount)
    def removeResource(self, player, resource, amount):
        self.players[player].removeResource(resource, amount)
    def countResources(self, player):
        return self.players[player].resourceCount()
    def getRandomResource(self, player):
        return self.players[player].getRandomResource()

    def getSurroundingResources(self, nodeid):
        return self.board.getSurroundingResources(nodeid)

    def addCard(self, player, card):
        self.players[player].addCard(card)
    def removeCard(self, player, card):
        self.players[player].removeCard(card)

    def getBuildings(self, dieroll):
        return self.board.getBuildings(dieroll)
    def updateAllScores(self):
        for i in xrange(0,len(self.players)):
            self.updateScore(i)

    def updateScore(self, player):
        c = self.board.getCount(player, 'city')
        s = self.board.getCount(player, 'settlement')
        army = 2 if (player == self.largestarmy) else 0
        road = 2 if (player == self.longestroad) else 0
        vpcards = self.players[player].cards['vp']
        self.players[player].score = c*2 + s + army + road

    def addBuilding(self, player, building, corner):
        self.board.addBuilding(corner, player, building)
    def addRoad(self, player, corner1, corner2):
        self.board.addRoad(corner1,corner2,player)
    def getLongestRoads(self):
        return self.board.getLongestRoad()
    # This could be too slow!! Called when things are built
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

    def getAdjacentPlayers(self, tile):
        return self.board.getAdjacentPlayers(tile)

    def setRobberTile(self, tile):
        self.board.setRobber(tile)
    def getRobberTile(self):
        return self.board.getRobberPos()
