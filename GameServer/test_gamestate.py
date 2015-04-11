from GameState import GameState
from visitor import StateVisitor

g = GameState(2)

g.addBuilding(0, 'settlement', 33)
g.addRoad(0, 33, 34)
g.addRoad(0, 34, 35)

g.addBuilding(1, 'settlement', 28)
g.addRoad(1, 28, 29)
g.addRoad(1, 29, 30)

g.addResource(0, 'ore', 2)
g.addResource(1, 'brick', 3)

g.updateScore(0)
g.updateScore(1)

v = StateVisitor()
g.accept(v)
print v.get_json()
