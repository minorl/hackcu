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
	def __init__():
		super()
		self.counter = 0
		self.curr = random.sample([-1,1], 1)[0]

	def getSensors(self):	
		obs = zeros(1)
		obs[0] = self.curr
		return obs

	def performAction(self, action):	
		print "Performing action: + " + str(action)
		self.counter += self.curr * numpy.sign(action[0])
		self.curr = random.sample([-1,1], 1)[0]

	def reset(self):
		self.counter = 0
