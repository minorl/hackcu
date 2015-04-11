from scipy import zeros, array
from pybrain.rl.environments.task import Task

class TestTask(Task):
	def __init__(self, environment):
		super()

	def getReward(self):
		return self.env.counter
