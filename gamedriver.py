from GameServer.controller import Controller
#from mlprototype.aiplayer import AIPlayer


P1 = 1 #AIPlayer()
P2 = 1 #AIPlayer()
P3 = 1 #AIPlayer()
P4 = 1 #AIPlayer()

while True:
    c = Controller([P1, P2, P3, P4])
    c.play()

