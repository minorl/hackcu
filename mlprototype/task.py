from scipy import zeros, array
from pybrain.rl.environments.episodic import EpisodicTask

class SettleTask(EpisodicTask):
    def __init__(self, environment):
        self.last = 0
        self.env = environment
        super(SettleTask, self).__init__(environment)

    def isFinished(self):
        return self.env.state.phase == "ended"

    def getReward(self):
        state = self.env.state
        return ((state.players[state.turn].score)**2) + 100 * (state.phase == "ended")
