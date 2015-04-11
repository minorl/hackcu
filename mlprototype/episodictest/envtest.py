from pybrain.rl.environments.environment import Environment
from scipy import zeros
from numpy import sign
import random

class TestEnv(Environment):
    random.seed()
    discreteStates = True
    discreteActions = True
    inDim = 1
    outDim = 1
    numActions = 2
    def __init__(self):
        super(TestEnv, self).__init__()
        self.good_actions = 0
        self.counter = 0
        self.date = 0
        self.curr = random.sample([-1,1], 1)[0]

    def getSensors(self):
        obs = zeros(1)
        obs[0] = self.curr
        return obs

    def performAction(self, action):
        increment = sign((action[0] - 0.5)*2) * sign(self.curr)
        if increment > 0:
            self.good_actions += 1
#            if self.good_actions % 50 == 0:
#                print "Good: %d" % self.good_actions
        self.counter += increment
        if self.counter < -100:
            self.counter = -100
        self.curr = random.sample([-1,1], 1)[0]
        self.date += 1

    def reset(self):
        self.counter = 0
        self.date = 0
