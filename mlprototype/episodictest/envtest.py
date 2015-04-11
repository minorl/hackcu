from pybrain.rl.environments.environment import Environment
from scipy import zeros
from numpy import sign
import random

class TestEnv(Environment):
    random.seed()
    discreteStates = True
    discreteActions = True
    inDim = 1
    outDim =1000
    numActions = 2
    def __init__(self):
        super(TestEnv, self).__init__()
        self.total = 0
        self.date = 0
        self.build_curr()

    def build_curr(self):
        self.curr = []
        for i in range(1000):
            self.curr.append(1 if random.random() > 0.5 else -1)

    def getSensors(self):
        return self.curr

    def performAction(self, action):
        for i in self.curr:
            self.total +=  (i * (action[0] - 1))/10
        self.build_curr()
        self.date += 1

    def reset(self):
        self.counter = 0
        self.date = 0
