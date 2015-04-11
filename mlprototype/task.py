from scipy import zeros, array
from pybrain.rl.environments.episodic import EpisodicTask

class SettleTask(EpisodicTask):
    def __init__(self, environment):
        self.counter = 0
        self.last = 0
        super(SettleTask, self).__init__(environment)

    def isFinished(self):
        self.counter += 1
        return self.counter % 1000 == 0

    def getReward(self):
        return 0
