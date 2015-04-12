from view_updater import *
from Validator import *
from GameState import *
from Move import *
import time

updater = ViewUpdater()
gs = GameState(4)
gs.phase = "standard"
updater.sendTiles(gs)

board = gs.board
board.addRoad(4,12,0)
updater.sendGameState(gs)
time.sleep(1)
corner1 = board.corners[12]
corner1.addBuilding(0,"settlement")
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(12,13,0)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(13,23,0)
updater.sendGameState(gs)
time.sleep(1)

board.addRoad(23,24,0)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(24,25,0)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(24,35,0)
updater.sendGameState(gs)
time.sleep(1)

board.addRoad(35,36,0)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(35,34,0)
updater.sendGameState(gs)
time.sleep(1)
corner2 = board.corners[34]
corner2.addBuilding(0,"settlement")
updater.sendGameState(gs)
time.sleep(1)
gs.board.setRobber("A")
updater.sendGameState(gs)
time.sleep(1)
gs.board.setRobber("B")
updater.sendGameState(gs)
time.sleep(1)
gs.board.setRobber("C")
updater.sendGameState(gs)
time.sleep(1)

board.addRoad(34,33,0)
updater.sendGameState(gs)
time.sleep(1)

board.addRoad(33,32,1)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(32,31,1)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(31,20,1)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(20,21,1)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(21,22,1)
updater.sendGameState(gs)
time.sleep(1)
board.addRoad(22,23,1)
updater.sendGameState(gs)
time.sleep(1)
corner3 = board.corners[23]
corner3.addBuilding(1,"settlement")
updater.sendGameState(gs)
time.sleep(1)

#board.getLongestRoad()
gs.players[0].resources['brick']=1
gs.players[0].resources['wood']=1
gs.players[0].resources['wheat']=1
gs.players[0].resources['sheep']=1
check = Validator(gs)
gs.phase = 'standard'
move1 = Move(0,'build',{'structure':'settlement', 'location':25})
updater.sendGameState(gs)
time.sleep(1)


gs.players[1].resources['ore']=3
gs.players[1].resources['wood']=1
gs.players[1].resources['wheat']=2
gs.players[1].resources['sheep']=1
check = Validator(gs)
move2 = Move(1,'build',{'structure':'city', 'location':34})

print check.validateMove(move1)
print check.validateMove(move2)
updater.sendGameState(gs)
time.sleep(1)

gs.phase = 'ended'
updater.sendGameState(gs)
time.sleep(1)




#print gs.board.setRobber('A')
#print len(board.edges)
