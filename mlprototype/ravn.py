from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import one_to_n

from scipy import argmax, array, r_, asarray, where

class RestrictedActionValueNetwork(ActionValueNetwork):
    def __init__(self, dimState, numActions, env, name=None):
        super(RestrictedActionValueNetwork, self).__init__(dimState, numActions, name)
        self.env = env

    def getActionValues(self, state):
        #valid_moves = get_moves(state)
        valid_moves = range(self.numActions)
        values = array([self.network.activate(r_[state, one_to_n(i, self.numActions)]) if i in valid_moves else np.NINF for i in range(self.numActions)])
        return values

    #operate on self.env
    def get_valid_moves(self):
        state = self.env.state
        whoami = state.turn
        if phase == "discard":
            return [ k for k in range(4) ]
        elif phase == "buildsettle":
        elif phase == "buildroad":
        elif phase == "moverobber":
        elif phase == "respondtrade":
        elif phase == "chooseplayer":
        elif phase == "standard":
# 0-4: Discard resource k
# 5-7: Choose player (whoami + k - 5) % 4
# 8-9: Decline/Accept trade
# 10-28: Move bandit to tile k - 5
# 29-82: Build settlement on node k-29
# 83-136: Upgrade settlement on node k - 83 to city
# 137-298: Build road from node (node k - 137)/3 in k%3th direction
# 299-352: place free settlement on node k - 299
# 353-514: place free road on (node k - 353)/3 in k%3th direction

