from GameState import GameState
from Validator import Validator
import random


class Controller(object):
    def __init__(self, players):
        self.players = players
        self.nplayers = len(players)
        self.state = GameState(self.nplayers)
        self.validator = Validator(self.state)

    def play(self):
        self.setup()
        while self.notEnded():
            self.roll() #resource/bandit
            self.takeTurn() #actions
            self.nextPlayerTurn()
        #Turn has 3 phases:
        #   Roll:
        #       If 7:
        #       If not:
        #   Action:
        #       Trade
        #       Build
        #       Play
        #   End


    def setup(self):
        #Decide first player randomly
        self.state.turn = random.randrange(0,self.nplayers)
        builtcount = 0
        while builtcount < self.nplayers * 2:
            self.state.phase = "buildsettle"
            self.updateView()
            move = self.getValidMove(self.state.turn)
            self.doMove(move)
            self.state.phase = "buildroad"
            self.updateView()
            move = self.getValidMove(self.state.turn)
            self.doMove(move)
            self.nextPlayerTurn()
            builtcount += 1
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
        pass

    def turnEnded(self):
        return self.state.phase == 'turnended'

    def roll(self):
        self.lastroll = random.randint(1,6) + random.randint(1,6)
        self.updateView()
        if self.lastroll == 7:
            turn = self.state.turn
            #resource discard
            for i in range(0, self.nplayers):
                self.state.turn = i
                nresources = self.state.countResources(i)
                if nresources > 7:
                    reqresources = nresources/2
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

    def moveRobber():
        self.state.phase = 'moverobber'
        move = self.getValidMove(self.state.turn)
        self.doMove(move)
        adjplayers = self.state.getAdjacentPlayer(self.state.getRobberTile())
        if self.turn in adjplayer: adjplayers.remove(self.turn)
        # Davis says to make code concise, use empty list as test for this
        # if statement otherwise he will hit irakli. I like irakli, so this list
        # is now the test for this if statement.
        if adjplayer:
            self.state.phaseinfo = adjplayer
            self.state.phase = 'chooseplayer'


    def getValidMove(self, player):
        self.updateView()
        move = self.players[player].getMove(self.state)
        # loop until valid move receied
        while not self.isValid(move):
            move = self.players[player].getMove(self.state)
        return move

    def isValid(self, move):
        return self.validator.validateMove(move)
