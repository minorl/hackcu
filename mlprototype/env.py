from pybrain.rl.environments.environment import Environment
from scipy import zeros
from numpy import sign
import threading

class SettleEnv(Environment):
    discreteStates = True
    discreteActions = True
    inDim = 1
    outDim = 1
    numActions = 2
    def __init__(self, cv, stateTransfer, actionTransfer):
        super(SettleEnv, self).__init__()
        self.cv = cv
        self.stateTransfer = stateTransfer
        self.actionTransfer = actionTransfer
        self.state = None
        #Have to bootstrap into the wait/notify cycle
        self.cv.acquire()
        #Signal that bootstrapping was successful
        self.actionTransfer[0] = True
        self.cv.wait()
        print "Rolling"

    def getSensors(self):
        print "Getting sensors"
        sensors = zeros(15)
        #Feature engineering
        
        return sensors
    def performAction(self, action):
        #choose move
        print "Applying action"
        self.actionTransfer[0] = 3
        self.cv.notify()
        self.cv.wait()
        self.cv.acquire()
        #actionTransfer[0] is now none
        #get new state
        self.state = self.stateTransfer[0]
        self.stateTransfer[0] = None

    def reset(self):
        pass
