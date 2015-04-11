from scipy import zeros, array
from pybrain.rl.environments.episodic import EpisodicTask
from numpy import sign

class TestTask(EpisodicTask):
    def __init__(self, environment):
        self.last = 0
        super(TestTask, self).__init__(environment)

    def getReward(self):
        if (100 < self.env.total < 200):
            return 100
        return 0

    def isFinished(self):
        done = self.env.date > 100
        return done
