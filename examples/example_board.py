from GameBoard import *
board = GameBoard()
board.addRoad(4,12,0)
corner1 = board.corners[12]
corner1.addBuilding(0,"settlement")
board.addRoad(12,13,0)
board.addRoad(13,23,0)

board.addRoad(23,24,0)
board.addRoad(24,25,0)
board.addRoad(24,35,0)

board.addRoad(35,36,0)
board.addRoad(35,34,0)
corner2 = board.corners[34]
corner2.addBuilding(0,"settlement")
board.addRoad(34,33,0)

board.addRoad(33,32,1)
board.addRoad(32,31,1)
board.addRoad(31,20,1)
board.addRoad(20,21,1)
board.addRoad(21,22,1)
board.addRoad(22,23,1)
corner3 = board.corners[23]
corner3.addBuilding(1,"settlement")

board.getLongestRoad()
print len(board.edges)