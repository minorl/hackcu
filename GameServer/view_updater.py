import GameState
from visitor import *

import socket
import json


#data = s.recv(1024)
#print "Received: " + json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class ViewUpdater(object):
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        port = 31337
        s.connect((host,port))

    def sendJSON(self, state):
        v = StateVisitor()
        state.accept(v)
        package = v.get_json()
        s.send(json.dumps(package))  