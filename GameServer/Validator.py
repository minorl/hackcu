import GameState

class Validator(object):
    def __init__(self,gameState):
        self.gameState = gameState
    def validateMove(self,move):
        if move.typ=="build":
            if not self.checkResources(move.playerid,move.structure):
                return False
            if 


    def checkResources(self, playerID,buildingTag):
        playerResources = self.gameState.players[playerID].resources
        if buildingTag == "settlement":
            return playerResources['brick']>=1 and playerResources['wood']>=1 and playerResources['wheat']>=1 and playerResources['sheep']>=1
        if buildingTag == "city":
            return playerResources['wheat']>=2 and playerResources['ore']>=3
        if buildingTag == "road":
            return playerResources['brick']>=1 and playerResources['wood']>=1
    def checkLocation(self,playerID, buildingTag, location):
        if buildingTag == "settlement":
            pass
        if buildingTag == "city":
            pass
        if buildingTag == "road":
            pass