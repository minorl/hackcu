from threading import Condition, Lock, Thread
from mlprototype.env import SettleEnv
from mlprototype.task import SettleTask
from mlprototype.ravn import RestrictedActionValueNetwork
from mlprototype.hackedexplorer import EpsilonHackedExplorer
from pybrain.rl.learners.valuebased import NFQ
from pybrain.rl.agents.learning import LearningAgent
from pybrain.rl.experiments.episodic import EpisodicExperiment
from GameServer.Player import Player

class AIPlayer(Player):
    def __init__(self):
        super(AIPlayer, self).__init__()
        #initialize ML thread
        self.cv = Condition()
        self.stateTransfer = [None]
        self.actionTransfer = [None]
e       mlThread = Thread(target=AIPlayer.mlDriver, args=(self.cv, self.stateTransfer, self.actionTransfer))
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
        action = self.actionTransfer[0]
        self.actionTransfer[0] = None
        return action

    @staticmethod
    def mlDriver(cv, stateTransfer, actionTransfer):
        #parameter setup
        #dimensionality of state argument (could be less than stateTransfer)
        stateDim = 1
        #Number of moves possible
        numMoves = 2
        env = SettleEnv(cv, stateTransfer, actionTransfer)
        task = SettleTask(env)
        controller = RestrictedActionValueNetwork(stateDim, numMoves)
        learner = NFQ()
        learner.explorer = EpsilonHackedExplorer(env)
        agent = LearningAgent(controller, learner)
        experiment = EpisodicExperiment(task, agent)
        while True:
            experiment.doEpisodes(100)
            agent.learn()
            agent.reset()
            print "Cycled"
