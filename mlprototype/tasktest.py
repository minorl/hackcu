from scipy import zeros, array
from pybrain.rl.environments.task import Task

class TestTask(Task):
	def __init__(self, environment):
		self.last = 0
		super(TestTask, self).__init__(environment)

	def getReward(self):
		res = self.env.counter - self.last
		self.last = self.env.counter
		return res
