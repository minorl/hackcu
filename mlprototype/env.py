from pybrain.rl.environments.environment import Environment
from scipy import zeros
from numpy import sign
import numpy as np
import threading
class SettleEnv(Environment):
    phaseDict = {}
    for i, name in enumerate(["discard", "buildsettle", "buildroad", "moverobber", "respondtrade", "chooseplayer", "standard", "ended"]):
        phaseDict[name] = i
    discreteStates = True
    discreteActions = True
    inDim = 1
    outDim = 352
    numActions = 361
    def __init__(self, cv, stateTransfer, actionTransfer):
        super(SettleEnv, self).__init__()
        self.cv = cv
        self.stateTransfer = stateTransfer
        self.actionTransfer = actionTransfer
        self.state = None
        #Have to bootstrap into the wait/notify cycle
        self.cv.acquire()
        #Signal that bootstrapping was successful
        self.actionTransfer[0] = True
        self.cv.wait()
        self.state = self.stateTransfer[0]
        self.valid_moves = []

    def getSensors(self):
        self.sensors = zeros(352)
        #print "Getting sensors"
        #Feature engineering
        whoami = self.state.turn
        board = self.state.board
        myState = self.state.players[whoami]
        i = 0
        #Points
        self.sensors[i] = myState.score
        i += 1

        #My Cards
        for resource in ["brick", "wood", "sheep", "wheat", "ore"]:
            self.sensors[i] = myState.resources[resource]
            i += 1

        #Phase
        self.sensors[i] = SettleEnv.phaseDict[self.state.phase]
        i += 1

        #Expected resources
        expectation, vertexpectation = SettleEnv.getExpectedResources(board)
        #shuffle the players so we are always first
        for pid in range(4):
            for resource in range(5):
                self.sensors[i] = expectation[(whoami+pid) % 4][resource]
                i += 1

        for vertex in range(len(board.corners)):
            for resource in range(5):
                self.sensors[i] = vertexpectation[vertex][resource]
                i += 1

        #distance to each vertex
        distances = SettleEnv.getDistances(board, whoami)
        for d in distances:
            self.sensors[i] = d
            i += 1
 
        return self.sensors
    #Returns a tuple of:
    #-2d array expectedresources[playerId][resourcetype]
    #-2d array vertexpectation[vertexId][resourcetype
    @staticmethod
    def getExpectedResources(board):
        resourceDict = {"brick" : 0, "wood" : 1, "sheep" : 2, "wheat" : 3, "ore" : 4} 
        def prob(x):
            return (6 - abs(7-x))/12
        res = [[0 for rec in range(5)] for pid in range(4)]
        ver = [[0 for rec in range(5)] for vertex in board.corners]
        for vertex in board.corners:
            pid = vertex.buildingPlayerID
            if vertex.buildingTag is not None:
                if vertex.buildingTag == "settlement":
                    multiplier = 1
                elif vertex.buildingTag == "city":
                    multiplier = 2
                else:
                    raise Exception("Bad building tag: " + str(buildingTag))
                for tile in vertex.tiles:
                    if tile.resource != 'desert':
                        res[pid][resourceDict[tile.resource]] += multiplier * prob(tile.number)
                        ver[vertex.nodeID][resourceDict[tile.resource]] += prob(tile.number)

        return (res, ver)

    @staticmethod
    def getDistances(board, playerId):
        distance = [100 for v in board.corners]
        searchPoints = []
        for v in board.corners:
            if v.buildingPlayerID == playerId:
                searchPoints.append(v.nodeID)
            else:
                for edge in v.edges:
                    if edge.playerID == playerId:
                        searchPoints.append(v.nodeID)

        for init in searchPoints:
            Q = [init]
            distance[init] = 0
            while len(Q) > 0:
                v = Q.pop()
                current = board.corners[v]
                for e in current.edges:
                    if e.hasRoad == False:
                        wCorner = e.corners[0] if current is e.corners[1] else e.corners[1]
                        if wCorner.buildingTag is None:
                            w = wCorner.nodeID
                            if distance[w] > distance[v] + 1:
                                distance[w] = distance[v] + 1
                                Q.insert(0, w)
        return distance

    def performAction(self, action):
        #choose move
        #print "Applying action"
        self.actionTransfer[0] = action[0]
        self.cv.notify()
        self.cv.wait()
        self.cv.acquire()
        #actionTransfer[0] is now none
        #get new state
        self.state = self.stateTransfer[0]
        if self.state.phase == "ended":
            print "Hit end state"
        self.stateTransfer[0] = None

    def reset(self):
        pass
