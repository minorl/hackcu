from scipy import zeros, array
from pybrain.rl.environments.episodic import EpisodicTask
from numpy import sign

class TestTask(EpisodicTask):
    def __init__(self, environment):
        self.last = 0
        super(TestTask, self).__init__(environment)

    def getReward(self):
        if (abs(self.env.counter) >= 20):
            print "Done: %d, %d" % (self.env.date, self.env.counter)
            return sign(self.env.counter) * 100  - self.env.date
        return 0

    def isFinished(self):
        done = abs(self.env.counter) >= 20
        return done
