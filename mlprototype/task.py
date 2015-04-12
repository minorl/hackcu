from scipy import zeros, array
from pybrain.rl.environments.episodic import EpisodicTask

class SettleTask(EpisodicTask):
    def __init__(self, environment):
        self.last = 0
        self.env = environment
        super(SettleTask, self).__init__(environment)

    def isFinished(self):
        if self.env.state.phase == "ended":
            print "Task says it's done"
            return True
        return False

    def getReward(self):
        state = self.env.state
        score = state.players[state.turn].score
        diff = score - self.last
        reward = diff * abs(diff)
        if state.phase == "ended":
            #win
            if score >= 10:
                reward += 50
            #loss or stalemate
            else:
                reward = score
        return score
