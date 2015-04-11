
class AIPlayer(Player):
    def __init__():
        super(Player, self).__init__()
        
        #initialize ML thread


    def getMove(state):
        self.lock.lock()
        stateTransfer[0] = state
        self.lock.unlock()
        while actionTransfer[0] == None:
            pass
        self.lock.lock()
        action = actionTransfer[0]
        actionTransfer[0] = None
        return action

    @staticmethod
    def mlDriver(lock, stateTransfer, actionTransfer):
        env = SettlersEnvironment(lock, stateTransfer, actionTransfer)
        task = SettlersTask(env)
        controller = RestrictedActionValueNetwork(stateDim, numMoves)
        learner = NFQ()
        agent = LearningAgent(controller, learner)
        experiment = Experiment(task, agent)
