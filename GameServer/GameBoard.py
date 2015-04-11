class GameBoard:
	def __init__(self):
		self.corners = []
		self.edges = {} #(id1,id2)->CornerEdge
	pass


class Corner:
	def __init__(self,nodeID):
		self.nodeID = nodeID
	def setEdges(self):
		pass

	def addBuilding(playerID, buildingType):
		pass
	pass

class Tile:
	def __init__(self,tileID, resource,number):
		self.tileID = tileID
		self.resource = resource
		self.number = number

class CornerEdge:
	def __init__(self,id1, id2):
		self.hasRoad = False
		self.corners = (id1, id2)
		self.playerID = None
	def addRoad(self, playerID):
		self.hasRoad = True
		self.playerID = playerID

edge = CornerEdge(0,3)
print edge.hasRoad, edge.playerID
edge.addRoad(2)
print edge.hasRoad, edge.playerID