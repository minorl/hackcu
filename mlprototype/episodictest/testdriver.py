from scipy import *
import sys, time

from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA, NFQ
from pybrain.rl.experiments.episodic import EpisodicExperiment
from pybrain.rl.environments import Task
from tasktest import TestTask
from envtest import TestEnv

env = TestEnv()
task = TestTask(env)

controller = ActionValueNetwork(200, 3)
learner = NFQ()
agent = LearningAgent(controller, learner)
experiment = EpisodicExperiment(task, agent)

i = 0
while True:
    experiment.doEpisodes(1)
    agent.learn()
    agent.reset()
    i += 1
    print "Cycle: %d" %i
    if i > 60:
        agent.learning = False

