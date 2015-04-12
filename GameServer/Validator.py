import GameState

class Validator(object):
    def __init__(self,gameState):
        self.gameState = gameState
    def validateMove(self,move):
        print move.typ, self.gameState.phase
        #Phases: discard, buildsettle, buildroad, moverobber, respondtrade, chooseplayer, standard
        if move.typ=="build" and (self.gameState.phase== 'buildsettle' or self.gameState.phase== 'buildroad'):
            if move.structure == 'city':
                return False
            if not self.checkLocation(move.playerid,move.structure,move.location,self.gameState.phase):
                return False
            return True
        elif move.typ=="build" and self.gameState.phase== 'standard':
            if not self.checkResources(move.playerid,move.structure):
                return False
            if not self.checkLocation(move.playerid,move.structure,move.location, 'standard'):
                return False
            return True
        elif move.typ == "robber" and self.gameState.phase == 'moverobber':
            return move.location != self.gameState.board.robberPos
        elif move.typ == "takecard" and self.gameState.phase == 'chooseplayer':
            if move.target ==move.playerid:
                return False
            robberLocation = self.gameState.board.robberPos
            for cornerID in self.gameState.board.tileTbl[robberLocation]:
                if self.gameState.board.corners[cornerID].buildingPlayerID == move.target:
                    return True
            return False
        elif move.typ == "endturn" and self.gameState.phase == 'standard':
            return True
        elif move.typ == "discard" and self.gameState.phase == 'discard':
            return self.gameState.players[move.playerid].resources[move.card] >0
        else:
            return False



    def checkResources(self, playerID,buildingTag):
        playerResources = self.gameState.players[playerID].resources
        if buildingTag == "settlement":
            return playerResources['brick']>=1 and playerResources['wood']>=1 and playerResources['wheat']>=1 and playerResources['sheep']>=1
        if buildingTag == "city":
            return playerResources['wheat']>=2 and playerResources['ore']>=3
        if buildingTag == "road":
            return playerResources['brick']>=1 and playerResources['wood']>=1
    def checkLocation(self,playerID, buildingTag, location, phase):
        
        if buildingTag == "settlement": #check location empty
            corner = self.gameState.board.corners[location]
            if corner.buildingTag!=None:
                return False
            for road in corner.edges: #Check empty adjacent Tiles
                nextCorner = road.corners[0] if corner is road.corners[1] else road.corners[1]
                if nextCorner.buildingTag!=None:
                    return False
            if phase == 'buildsettle':
                return True
            hasRoad = False
            for road in corner.edges: #Next to Color Road
                if road.playerID==playerID:
                    hasRoad = True
            if not hasRoad:
                return False
            return True
        if buildingTag == "city":
            corner = self.gameState.board.corners[location]
            return corner.buildingTag=="settlement" and corner.buildingPlayerID == playerID
        if buildingTag == "road":
            road = self.gameState.board.getEdge(location[0],location[1])
            if road.hasRoad:
                return False
            hasConnection = False
            if road.corners[0].buildingPlayerID == playerID:
                return True
            if road.corners[1].buildingPlayerID == playerID:
                return True
            if road.corners[0].buildingTag == None and self.gameState.board.hasColorRoad(road.corners[0].nodeID,playerID):
                return True
            if road.corners[1].buildingTag == None and self.gameState.board.hasColorRoad(road.corners[1].nodeID,playerID):
                return True
            return False
