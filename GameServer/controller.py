from GameState import GameState
from Validator import Validator
from view_updater import ViewUpdater
import random
import logging

class Controller(object):
    def __init__(self, players):
        self.players = players
        self.nplayers = len(players)
        self.state = GameState(self.nplayers)
        self.validator = Validator(self.state)
        self.logger = logging.getLogger(__name__)
        self.update = ViewUpdater()

    def play(self):
        self.setup()
        while self.notEnded():
            self.roll() #resource/bandit
            self.takeTurn() #actions
            self.nextPlayerTurn()

    def setup(self):
        # Send initial state for display
        self.update.sendTiles(self.state)
        #Decide first player randomly
        self.state.turn = random.randrange(0,self.nplayers)
        builtcount = 0
        while builtcount < self.nplayers*2:
            self.state.phase = "buildsettle"
            self.updateView()
            bs_move = self.getValidMove(self.state.turn)
            self.doMove(bs_move)
            self.state.phase = "buildroad"
            self.updateView()
            move = self.getValidMove(self.state.turn)
            self.doMove(move)
            #if this is second settle built do resource init
            if builtcount >= self.nplayers:
                for rec in self.state.getSurroundingResources():
                    self.state.addResource(self.state.turn, rec, bs_move.location)
            self.nextPlayerTurn()
            builtcount += 1
        #initial resource allocation

        self.state.phase = 'standard'

    def nextPlayerTurn(self):
        self.state.turn = (self.state.turn + 1) % self.nplayers

    def takeTurn(self):
        #loop action (trade, build, play, buy) until turn ended
        while not self.turnEnded():
            self.updateView()
            move = self.getValidMove(self.state.turn)
            self.doMove(move)
        self.state.phase = 'standard'

    def updateView(self):
        self.update.sendGameState(self.state)

    def turnEnded(self):
        return self.state.phase == 'turnended'

    def roll(self):
        self.state.lastroll = random.randint(1,6) + random.randint(1,6)
        self.updateView()
        if self.state.lastroll == 7:
            turn = self.state.turn
            #resource discard
            for i in range(0, self.nplayers):
                self.state.turn = i
                nresources = self.state.countResources(i)
                if nresources > 7:
                    reqresources = (nresources+1)/2
                    self.state.phase = "discard"
                    while nresources > reqresources:
                        # number you need to discard
                        self.state.phaseinfo = nresources - reqresources
                        # should we change whose turn it is in state?
                        move = self.getValidMove(i)
                        self.doMove(move)
                        nresources = self.state.countResources(i)
            self.state.turn = turn
            #robber movement
            self.moveRobber()
        else: #resource collection
            for (r,p,b) in self.state.getBuildings(self.lastroll):
                mult = 1 if b == 'settlement' else 2
                self.state.addResource(p, r, mult)
            self.updateView()
        self.state.phase = 'standard'

    def moveRobber(self):
        self.state.phase = 'moverobber'
        move = self.getValidMove(self.state.turn)
        self.doMove(move)
        #list of playerid's next to robber
        adjplayers = self.state.getAdjacentPlayer(self.state.getRobberTile())
        if self.state.turn in adjplayer:
            adjplayers.remove(self.turn)
        #remove players who have no cards from adjacent list
        for i in xrange(len(adjplayers) - 1, -1, -1):
            if self.state.countResources(adjplayers[i]) == 0:
                del adjplayers[i]

        # Davis says to make code concise, use empty list as test for this
        # if statement otherwise he will hit irakli. I like irakli, so this list
        # is now the test for this if statement.
        if adjplayer:
            self.state.phaseinfo = adjplayer
            self.state.phase = 'chooseplayer'
            move = self.getValidMove()
            self.doMove(move)

    def getValidMove(self, player):
        self.updateView()
        move = self.players[player].getMove(self.state)
        # loop until valid move receied
        while not self.isValid(move):
            self.logger.error("INVALID MOVE RECEIVED: Player %d" % player)
            move = self.players[player].getMove(self.state)
        return move

    def isValid(self, move):
        return self.validator.validateMove(move)

    def doMove(self, move):
        if move.typ == 'build':
            if move.structure == 'road':
                # 1 brick, 1 wood
                self.state.addRoad(move.playerid, move.location[0], move.location[1])
                self.state.removeResource(move.playerid, 'brick', 1)
                self.state.removeResource(move.playerid, 'wood', 1)
            else:
                if move.structure == 'settlement':
                    # 1 brick, 1 wood, 1 wheat, 1 sheep settlement
                    self.state.removeResource(move.playerid, 'wood', 1)
                    self.state.removeResource(move.playerid, 'wheat', 1)
                    self.state.removeResource(move.playerid, 'brick', 1)
                    self.state.removeResource(move.playerid, 'sheep', 1)
                elif move.structure == 'city':
                    # 2 wheat, 3 ore city
                    self.state.removeResource(move.playerid, 'wheat', 2)
                    self.state.removeResource(move.playerid, 'ore', 3)
                else:
                    self.logger.error("Unrecognized build type %s" % move.structure)
                self.state.addBuilding(move.playerid, move.structure, move.location)
            # check to see if building changed longest road count
            l = self.state.getLongestRoads()
            currentlongest = 0
            if self.state.longestroad is not None:
                currentlongest = l[self.state.longestroad]
            newlongestid = None
            for i in xrange(0, self.nplayers):
                if l[i] > currentlongest:
                    newlongestid = i
                    currentlongest = l[i]
            #need to check if road breaking resulted in a tie
            if newlongestid != self.state.longestroad:
                if currentlongest<5:
                    self.state.longestroad = None
                elif l.count(currentlongest) != 1:
                    self.state.longestroad = None
                else:
                    self.state.longestroad = newlongestid
            # update remaining building count
            self.state.updateRemaining(move.playerid)
            self.updateView()
        elif mov.typ == 'trade':
            self.logger.error("TRADE MOVE NOT SUPPORTED")
        elif mov.typ == 'robber':
            #set robber tile
            self.state.setRobberTile(move.location)
        elif mov.typ == 'takecard':
            # Remove card from target, add to initiator
            rectoremove = self.state.getRandomResource()
            self.state.removeResource(move.target, rectoremove, 1)
            self.state.addResource(move.playerid, rectoremove, 1)
            self.updateView()
        elif mov.typ == 'playcard':
            #yell when things are important
            self.logger.error("PLAY CARD MOVE NOT SUPPORTED")
        elif mov.typ == 'discard':
            # Need to add ability to discard more than one at a time
            self.state.removeResource(move.playerid, move.card)
        elif mov.typ == 'endturn':
            self.state.phase = 'endturn'

