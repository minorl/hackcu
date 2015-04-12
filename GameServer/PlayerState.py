import random

class PlayerState(object):
    """Holds state for players"""
    def __init__(self, num):
        self.playerid = num #int
        self.score = 0
        self.resources = {"brick" : 0, "wood" : 0, "sheep" : 0, "wheat" : 0, "ore" : 0}
        self.trade = {"brick" : 0, "wood" : 0, "sheep" : 0, "wheat" : 0, "ore" : 0}
        self.cards = {"knight":0, "vp":0, "roadbuilding":0, "yearofplenty":0, "monopoly": 0}
        self.startingBuildings = {"city":4, "settlement":5, "road":15}
        self.remBuildings = {"city":4, "settlement":5, "road":15}

    def addResource(self, resource, amount):
        self.resources[resource] += amount
    def removeResource(self, resource, amount):
        self.resources[resource] -= amount
    def addCard(self, card):
        self.cards[card] += 1
    def removeCard(self, card):
        self.cards[card] -= 1
    def getRandomResource(self):
        reclist = []
        for (rec, n) in self.resourceCount:
            reclist += [rec]*n
        return random.sample(reclist, 1)[0]
    def resourceCount(self):
        return sum(self.resources.itervalues())
    def getScore(self):
        return self.score
    def accept(self, visitor):
        visitor.visit(self)






