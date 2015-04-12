from threading import Condition, Lock, Thread
from mlprototype.env import SettleEnv
from mlprototype.task import SettleTask
from mlprototype.ravn import RestrictedActionValueNetwork
from mlprototype.ravn import resourceList
from mlprototype.hackedexplorer import EpsilonHackedExplorer
from pybrain.rl.learners.valuebased import NFQ
from pybrain.rl.agents.learning import LearningAgent
from pybrain.rl.experiments.episodic import EpisodicExperiment
from GameServer.Player import Player
from GameServer.Move import Move

class AIPlayer(Player):
    def __init__(self):
        super(AIPlayer, self).__init__()
        #initialize ML thread
        self.cv = Condition()
        self.stateTransfer = [None]
        self.actionTransfer = [None]
        mlThread = Thread(target=AIPlayer.mlDriver, args=(self.cv, self.stateTransfer, self.actionTransfer) )
        mlThread.start()
        #Need to bootstrap into the lock handoff
        while self.actionTransfer[0] is None:
            pass
        self.cv.acquire()

    def getMove(self, state):
        print "Setting state"
        self.stateTransfer[0] = state
        self.cv.notify()
        self.cv.wait()
        self.cv.acquire()
        #Translate action from number to actual move
        action = self.actionTransfer[0]
        self.actionTransfer[0] = None
        whoami = state.turn
        #Discard
        action = int(action)
        if i in range(0,5):
            move = Move(whoami, 'discard', {'card':resourceList[i]})
        #Choose player
        elif action in range(5, 8):
            target = ((action - 4) + whoami) % 4
            move = Move(whoami, 'takecard', {'target' : target})
        #no or yes to trade
        elif action in range(8,10):
            raise Exception("Tried to respond to trade, not implemented.")
        # move bandit
        elif action in range(10, 29):
            move = Move(whoami, 'robber', {'location': chr(ord('A') + action - 10)})
        # build settlement
        elif action in range(29, 83) or action in range(209, 263):
            if action < 83:
                target = action - 29
            else:
                target = action - 209
            print "Player: %d building settlement at %d" % (whoami, target)
            move = Move(whoami, 'build', {'location' : target, 'structure' : 'settlement'})
        # upgrade settlement
        elif action in range(83, 137):
            move = Move(whoami, 'build', {'location' : action - 83, 'structure' : 'city'})
        # build road
        elif action in range(137,209) or action in range (263,335):
            if action < 209:
                _, edge = state.board.edges.items()[action-137]
            else:
                _, edge = state.board.edges.items()[action-263]
            v1,v2 = edge.corners
            print "Player: %d building road from %d->%d" % (whoami, v1.nodeID, v2.nodeID)
            move = Move(whoami, 'build', {'location' : (v1.nodeID, v2.nodeID), 'structure' : 'road'})
        # build free settlement
        elif action in range(209, 263):
            move = Move(whoami, 'build', {'location' : action - 209, 'structure' : 'settlement'})
        elif action == 335:
            move = Move(whoami, 'endturn')
        else:
            raise Exception("Unrecognized action: %d" % action)

        return move

    @staticmethod
    def mlDriver(cv, stateTransfer, actionTransfer):
        #parameter setup
        #dimensionality of state argument (could be less than stateTransfer)
        stateDim = 352
        #Number of moves possible
        numMoves = 356
        env = SettleEnv(cv, stateTransfer, actionTransfer)
        task = SettleTask(env)
        controller = RestrictedActionValueNetwork(stateDim, numMoves, env)
        learner = NFQ()
        learner.explorer = EpsilonHackedExplorer(env)
        agent = LearningAgent(controller, learner)
        experiment = EpisodicExperiment(task, agent)
        while True:
            experiment.doEpisodes(100)
            agent.learn()
            agent.reset()
            print "Cycled"
