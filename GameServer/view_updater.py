import GameState
from visitor import *

import socket
import json


#data = s.recv(1024)
#print "Received: " + json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class ViewUpdater(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(None)
        host = 'localhost'
        port = 31337
        self.s.connect((host,port))

    def sendGameState(self, state):
        v = StateVisitor()
        state.accept(v)
        package = v.get_json()
        print package
        self.s.send(package)

    def sendTiles(self, state):
        v = InitialStateVisitor()
        state.accept(v)
        package = v.get_json()
        yyself.s.send(package)

    def reinitialize(self):
        host = 'localhost'
        port = 31337
        self.s.connect((host,port))
