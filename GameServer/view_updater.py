import GameState
from visitor import *

import socket
import json


class ViewUpdater(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(None)
        self.acker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.acker.settimeout(None)

        host = 'localhost'
        port = 31337

        self.s.connect((host,port))
        self.acker.connect((host,port+1))

    def sendGameState(self, state):
        v = StateVisitor()
        state.accept(v)
        package = v.get_json()
        self.s.send(package)
        self.waitForAck()

    def waitForAck(self):
        bytes_rec = 0
        while bytes_rec < 3:
            rec = self.acker.recv(512)
            bytes_rec += len(rec)

    def sendTiles(self, state):
        v = InitialStateVisitor()
        state.accept(v)
        package = v.get_json()
        self.s.send(package)
        self.waitForAck()

    def reinitialize(self):
        host = 'localhost'
        port = 31337
        self.s.connect((host,port))
