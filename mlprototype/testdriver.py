from scipy import *
import sys, time

from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA, NFQ
from pybrain.rl.experiments import Experiment
from pybrain.rl.environments import Task
from tasktest import TestTask
from envtest import TestEnv

env = TestEnv()
task = TestTask(env)

controller = ActionValueNetwork(1, 2)
learner = NFQ()
agent = LearningAgent(controller, learner)
experiment = Experiment(task, agent)

while True:
	experiment.doInteractions(100)
	agent.learn()
	agent.reset()
	print "Cycle"
