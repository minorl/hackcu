from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import one_to_n

from scipy import argmax, array, r_, asarray, where

class RestrictedActionValueNetwork(Module, ActionValueNetwork):
    def __init__(self, dimState, numActions, name=None):
        super(RestrictedActionValueNetwork, self).__init__(dimState, numActions, name)

    def getActionValues(self, state):
        valid_moves = get_moves(state)
        values = array([self.network.activate(r_[state, one_to_n(i, self.numActions)]) if i in valid_moves else np.NINF for i in range(self.numActions)])
        return values
