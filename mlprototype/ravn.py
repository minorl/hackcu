from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import one_to_n

from scipy import argmax, array, r_, asarray, where
import numpy as np

resourceList = ["brick", "wood", "sheep", "wheat", "ore"]

class RestrictedActionValueNetwork(ActionValueNetwork):
    def __init__(self, dimState, numActions, env, name=None):
        super(RestrictedActionValueNetwork, self).__init__(dimState, numActions, name)
        self.env = env

    def getActionValues(self, state):
        #valid_moves = get_moves(state)
        #valid_moves = range(self.numActions)
        valid_moves = self.get_valid_moves()
        values = array([self.network.activate(r_[state, one_to_n(i, self.numActions)]) if i in valid_moves else np.NINF for i in range(self.numActions)])
        return values

    #operate on self.env
    def get_valid_moves(self):
        state = self.env.state
#        print "RAVN State: " + str(state)
        board = state.board
        whoami = state.turn
        phase = state.phase
        if phase == "ended":
            moves = [0]
        elif phase == "discard":
            print "Discarding"
            resources = state.players[whoami].resources
            moves = [ k for k in range(5) if  resources[resourceList[k]] > 0]
        elif phase == "buildsettle":
            valid = RestrictedActionValueNetwork.validSettleLocations(board)
            moves = [ k + 209 for k in range(54) if valid[k]]
        elif phase == "buildroad":
            #identify settlement that has no road yet
            found = None
            for v in board.corners:
                if v.buildingPlayerID == whoami:
                    hasRoad = False
                    for e in v.edges:
                        hasRoad |= e.hasRoad
                    if not hasRoad:
                        found = v
                        break

            indices = []
            edgeList = [e for _,e in board.edges.items()]
            for e in found.edges:
                indices.append(edgeList.index(e))
            indices.sort()
            moves = [k + 263 for k in indices]

        elif phase == "moverobber":
            print "Moving robber"
            #get robber location
            moves = []
            for i in range(0,19):
                if ord(board.robberPos) != ord('A') + i:
                    moves += [10 + i]
        elif phase == "respondtrade":
            raise Exception("naw fuck that")
            moves = [8,9]
        elif phase == "chooseplayer":
            print "Choosing player"
            #state.phaseInfo is list of player ints
            rotated = [(k - whoami)%4 for k in state.phaseinfo]
            moves = [k + 4 for k in rotated]
        elif phase == "standard":
            moves = []
            myState = state.players[whoami]
            myResources = myState.resources
            #Get list of my settlements
            mySettles = []
            for v in board.corners:
                if v.buildingPlayerID == whoami:
                    mySettles.append(v)

            #Build up a set of reachable nodes form my settlements
            reachable = set([])
            for index in board.corners:
                if len(reachable) is None or not v.nodeID in reachable:
                    reachable |= set(RestrictedActionValueNetwork.getLinkedNodes(board, v.nodeID, whoami))

            #Locations with a large enough radius to settle at
            validBool = RestrictedActionValueNetwork.validSettleLocations(board)
            valid = set([k for k in range(54) if validBool[k]])

            #Check for city upgrades
            if myResources["ore"] >= 3 and myResources["wheat"] >= 2:
                for v in mySettles:
                    if v.buildingTag != "city":
                        moves.append(83 + v.nodeID)

            #build settlement
            if myResources["wood"] >= 1 and myResources["sheep"] >= 1 and myResources["brick"] >= 1 and myResources["wheat"] >= 1:
                for nodeID in valid & reachable:
                    moves.append(nodeID + 29)

            #build road
            for (i,(_,edge)) in enumerate(board.edges.items()):
                v,w = edge.corners
                if not edge.hasRoad and v in reachable or w in reachable:
                    moves.append(137 + i)

            moves.append(335)

        else:
            raise Exception("Unrecognized phase: " + str(phase))

        moves.sort()
        self.env.valid_moves = moves
        return moves

    @staticmethod
    def validSettleLocations(board):
        valid = [True for i in range(54)]
        for v in board.corners:
            if v.buildingTag is not None:
                for edge in v.edges:
                    for node in edge.corners:
                        valid[node.nodeID] = False
        return valid

    #initial is a nodeID
    @staticmethod
    def getLinkedNodes(board, initial, playerID):
        Q = [initial]
        visited = [False for k in range(54)]
        while len(Q) > 0:
            v = Q.pop()
            current = board.corners[v]
            for e in current.edges:
                if e.hasRoad and e.playerID == playerID:
                    wCorner = e.corners[0] if current is e.corners[1] else e.corners[1]
                    w = wCorner.nodeID
                    if not visited[w]:
                        visited[w] = True
                        Q.insert(0,w)
        return [k for k in range(54) if visited[k]]

# 0-4: Discard resource k
# 5-7: Choose player (whoami + k - 5) % 4
# 8-9: Decline/Accept trade
# 10-28: Move bandit to tile k - 5
# 29-82: Build settlement on node k-29
# 83-136: Upgrade settlement on node k - 83 to city
# 137-208: Build k-137th road according to board.edges
# 209-262: place free settlement on node k - 209
# 263-334: place free k-263rd road
# 335: end turn
