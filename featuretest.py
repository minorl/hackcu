from GameServer.test_gamestate import makeTest
from mlprototype.env import SettleEnv

env = SettleEnv(None, [None], [None])
env.state = makeTest()
env.getSensors()
