from GameServer.controller import Controller
from mlprototype.aiplayer import AIPlayer
from GameServer.view_updater import ViewUpdater

P1 = AIPlayer()
P2 = AIPlayer()
P3 = AIPlayer()
P4 = AIPlayer()
update = ViewUpdater()

while True:
    c = Controller([P1, P2, P3, P4], update)
    c.play()

