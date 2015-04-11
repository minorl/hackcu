import abc
#Interface for players
class Player(object):
    @abc.abstractmethod
    def getMove(self, state):
        return
