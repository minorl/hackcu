class PlayerState(object):
    """Holds state for players"""
    def __init__(self, num):
        self.playerid = num
        self.score = 0
        self.resources = {"brick" : 0, "wood" : 0, "sheep" : 0, "wheat" : 0, "ore" : 0}
        self.trade = {"brick" : 0, "wood" : 0, "sheep" : 0, "wheat" : 0, "ore" : 0}
        self.cards = []
    def addResource(self, resource, amount):
        self.resources[resource] += amount
    def removeResource(self, resource, amount):
        self.resources[resource] -= amount
    def resourceCount(self):
        return sum(self.resources.itervalues())
    def getScore(self):
        return self.score
    def accept(self, visitor):
        visitor.visit(self)






