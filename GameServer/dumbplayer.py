from GameServer.Player import Player
from GameServer.Move import Move

class DumbPlayer(Player):
    def __init__(self, seed):
        super(DumbPlayer, self).__init__()
        self.pid = seed
        if seed == 0:
            self.settle1 = 9
            self.settle2 = 49
            self.roadpath= [9,19,18, 29, 28]
        elif seed == 1:
            self.settle1 = 11
            self.settle2 = 51
            self.roadpath = [11, 21, 20, 31, 30]
        elif seed == 2:
            self.settle1 = 13
            self.settle2 = 53
            self.roadpath = [13, 23, 22, 33, 32]
        elif seed == 3:
            self.settle1 = 15
            self.settle2 = 47
            self.roadpath = [15,25,24,35,34]
        self.roadsbuilt = 0
        self.turncount = 0
    def getMove(self, state):
        if self.turncount == 0:
            self.turncount += 1
            return Move(self.pid, 'build', {'structure':'settlement', 'location':self.settle1})
        elif self.turncount == 1:
            self.turncount  += 1
            self.roadsbuilt += 1
            return Move(self.pid, 'build', {'structure':'road', 'location':(self.roadpath[0], self.roadpath[1])})
        elif self.turncount == 2:
            self.turncount  += 1
            return  Move(self.pid, 'build', {'structure':'settlement', 'location':self.settle2})
        elif self.turncount == 3:
            self.turncount +=1
            self.roadsbuilt += 1
            return Move(self.pid, 'build', {'structure':'road', 'location':(self.roadpath[1], self.roadpath[2])})
        elif self.turncount >= 4:
            return self.chooseMove(state)
    def chooseMove(self, state):
        if state.phase == 'moverobber':
            t  = state.getRobberTile()
            if t == 'P':
                tar = 'H'
            else:
                tar = 'P'
            return Move(self.pid, 'robber', {'location': tar})
        elif (self.roadsbuilt < 4 and state.players[self.pid].resources['brick'] >= 1 and state.players[self.pid].resources['wood'] >= 1):
            m = Move(self.pid, 'build', {'structure':'road', 'location':(self.roadpath[self.roadsbuilt], self.roadpath[self.roadsbuilt+1])})
            self.roadsbuilt += 1
            return m
        elif state.phase == 'chooseplayer':
            return Move(self.pid, 'takecard', {'target':self.phaseinfo[0]})
        elif state.phase == 'discard':
            if state.players[self.pid].resources['ore'] > 0:
                res = 'ore'
            elif state.players[self.pid].resources['sheep'] > 0:
                res= 'sheep'
            elif state.players[self.pid].resources['wheat'] > 0:
                res = 'wheat'
            elif state.players[self.pid].resources['wood'] > 0:
                res = 'wood'
            else:
                res = 'brick'
                
            return Move(self.pid, 'discard', {'card':res})
        elif state.phase == 'ended':
            self.turncount = 0
            self.roadsbuilt = 0
        else:
            return Move(self.pid, 'endturn', {})







