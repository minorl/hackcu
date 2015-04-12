from GameServer.controller import Controller
from mlprototype.aiplayer import AIPlayer
from GameServer.view_updater import ViewUpdater
from GameServer.dumbplayer import DumbPlayer
import time
import logging
import numpy
import json


def moving_average(l):
    if len(l) < 10:
        avg = sum(l)/len(l)
    else:
        avg = sum(l[-10:])/10
    return avg


logging.basicConfig(level=10, format="%(asctime)s;%(levelname)s;%(message)s", datefmt= "%H:%M:%S")
logger = logging.getLogger(__name__)

logger.debug("Initializing players")

P1 = AIPlayer()
P2 = AIPlayer()
P3 = AIPlayer()
P4 = AIPlayer()
update = ViewUpdater()

logger.debug("Players initialized, starting game")
previous_games = []
print "Games Completed \t Turns \t Last 10 Average Turns \t Average"
data_dict = {'games_completed':0, 'last_game_turns':0, 'last_10_avg': 0, 'all_game_avg':0}

while True:
    c = Controller([P1, P2, P3, P4], update)
    c.play()
    logger.debug("Game ended, starting new game")
    data_dict['games_completed'] += 1
    previous_games.append(c.state.numturns)
    time.sleep(5) 
    
    data_dict['last_game_turns'] = c.state.numturns
    data_dict['last_10_avg'] = moving_average(previous_games)
    data_dict['all_game_avg'] = int(numpy.mean(previous_games))

    print "%d \t %d \t %d \t %d" % (data_dict['games_completed'], data_dict['last_game_turns'], data_dict['last_10_avg'], data_dict['all_game_avg'])
    
    #update.s.send(json.dumps({'stats': data_dict}))
    #Waiting for ack
    #update.waitForAck()
    

