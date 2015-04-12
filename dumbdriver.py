from GameServer.controller import Controller
from GameServer.view_updater import ViewUpdater
from GameServer.dumbplayer import DumbPlayer
import time
import logging

logging.basicConfig(level=10, format="%(asctime)s;%(levelname)s;%(message)s", datefmt= "%H:%M:%S")
logger = logging.getLogger(__name__)

logger.debug("Initializing players")

P1 = DumbPlayer(0)
P2 = DumbPlayer(1)
P3 = DumbPlayer(2)
P4 = DumbPlayer(3)
update = ViewUpdater()

logger.debug("Players initialized, starting game")

while True:
    c = Controller([P1, P2, P3, P4], update)
    c.play()
    logger.debug("Game ended, starting new game")
    time.sleep(5)
