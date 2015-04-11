import GameState

class Validator(object):
    def __init__(self,gameState):
        self.gameState = gameState
    def validateMove(self,move):
        if move.typ=="build":
            #if not self.checkResources(move.playerid,move.structure):
            #    return False
            if not self.checkLocation(move.playerid,move.structure,move.location):
                return False


    def checkResources(self, playerID,buildingTag):
        playerResources = self.gameState.players[playerID].resources
        if buildingTag == "settlement":
            return playerResources['brick']>=1 and playerResources['wood']>=1 and playerResources['wheat']>=1 and playerResources['sheep']>=1
        if buildingTag == "city":
            return playerResources['wheat']>=2 and playerResources['ore']>=3
        if buildingTag == "road":
            return playerResources['brick']>=1 and playerResources['wood']>=1
    def checkLocation(self,playerID, buildingTag, location):
        
        if buildingTag == "settlement": #check location empty
            corner = self.gameState.board.corners[location]
            if corner.buildingTag!=None:
                return False
            for road in corner.edges: #Check empty adjacent Tiles
                nextCorner = road.corners[0] if corner is road.corners[1] else road.corners[1]
                if nextCorner.buildingTag!=None:
                    return False
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
