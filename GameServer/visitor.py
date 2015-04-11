from GameState import GameState
from PlayerState import PlayerState
from GameBoard import GameBoard, Corner, Tile

class visitor(object):
    def __init__(self):
        pass
    def visit(self, obj):
        if isinstance(obj, GameBoard):
            self.visit_board(obj)
        elif isinstance(obj, PlayerState):
            self.visit_player(obj)
        elif isinstance(obj, Tile):
            self.visit_tile(obj)
        elif isinstance(obj, GameState):
            self.visit_gamestate(obj)
        elif isinstance(obj, Corner):
            self.visit_corner(obj)
        else:
            raise Exception("Unrecognized obj in visitor %s" % str(s))
    def visit_gamestate(self, obj):
        pass
    def visit_playerstate(self, obj):
        pass
    def visit_board(self, obj):
        pass
    def visit_tile(self, obj):
        pass
    def visit_corner(self, obj):
        pass

class InitialStateVisitor(visitor):
    def __init__(self):
        super(InitialStateVisitor, self).__init__()
        self.initial_tiles = 19*[None]
        #L-R T-B for drawing purposes
        self.loc_lookup = {
                'A' :0, 'L':1, 'K':2, 'B':3, 'M' : 4, 'R': 5, 'J' : 6,
                'C':7, 'N':8, 'S':9, 'Q':10, 'I':11, 'D':12, 'O':13,
                'P':15, 'H':15, 'E':16, 'F':17, 'G':18
                }
    def visit_gamestate(self, obj):
        pass
    def visit_playerstate(self, obj):
        pass
    def visit_board(self, obj):
        pass
    def visit_tile(self, obj):
        dict_rep = {'id' :obj.tileID, 'resource':obj.resource, 'dienum' : obj.number}
        self.initial_tiles[self.loc_lookup[obj.tileID]] = dict_rep
    def visit_corner(self, obj):
        pass
