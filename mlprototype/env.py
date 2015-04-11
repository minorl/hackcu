from pybrain.rl.environments.environment import Environment
from scipy import zeros
from numpy import sign

class SettleEnv(Environment):
    discreteStates = True
    discreteActions = True
    inDim = 1
    outDim = 1
    numActions = 2
    def __init__(self, lock, stateTransfer):
        super(SettleEnv, self).__init__()
        self.lock = lock
        self.stateTransfer = stateTransfer
        self.actionTransfer = actionTransfer

    def getSensors(self):
        obs = zeros(1)
        obs[0] = self.curr
        return obs

    def performAction(self, action):
        #choose move
        actionTransfer[0] = #chosen move
        stateTransfer[0] = None
        self.lock.unlock()
        while stateTransfer[0] == None:
            pass
        self.lock.lock()
        #actionTransfer[0] is now none
    def reset(self):
        self.counter = 0

