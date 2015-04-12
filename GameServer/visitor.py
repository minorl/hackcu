from GameState import GameState
from PlayerState import PlayerState
from GameBoard import GameBoard, Corner, Tile, CornerEdge
import json
class visitor(object):
    def __init__(self):
        pass
    def visit(self, obj):
        if isinstance(obj, GameBoard):
            self.visit_board(obj)
        elif isinstance(obj, PlayerState):
            self.visit_playerstate(obj)
        elif isinstance(obj, Tile):
            self.visit_tile(obj)
        elif isinstance(obj, GameState):
            self.visit_gamestate(obj)
        elif isinstance(obj, Corner):
            self.visit_corner(obj)
        elif isinstance(obj, CornerEdge):
            self.visit_edge(obj)
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
    def visit_edge(self, obj):
        pass

class StateVisitor(visitor):
    def __init__(self):
        super(StateVisitor, self).__init__()
        nCorners = 54
        maxPlayers = 4
        nEdges = 72

        self.state = {"corner_states" : [None]*nCorners, "player_states" : [None]*maxPlayers, "edge_states" : [] }
    def visit_gamestate(self, obj):
        self.state["longest_road"] = obj.longestroad
        self.state["largest_army"] = obj.largestarmy
        self.state["turn"] = obj.turn
        self.state["last_roll"] = obj.lastroll
        self.state["phase"] = obj.phase
        self.state["phase_info"] = obj.phaseinfo
        self.state["turn_number"] = obj.numturns
    def visit_playerstate(self, obj):
        player_rep = {"id" : obj.playerid, "score" : obj.score, "resources" : obj.resources, "trade" : obj.trade, "cards" : obj.cards, "remaining_buildings" : obj.remBuildings}
        self.state["player_states"][obj.playerid] = player_rep
    def visit_board(self, obj):
        self.state["robber"] = obj.robberPos
    def visit_corner(self, obj):
        corner_rep = {"id": obj.nodeID, "building_tag": obj.buildingTag, "player_id": obj.buildingPlayerID}
        self.state["corner_states"][obj.nodeID] = corner_rep
    def visit_edge(self, obj):
        #edge corners is sorted
        edge_rep = {"player_id":obj.playerID if obj.hasRoad else None, "corners" : [obj.corners[0].nodeID, obj.corners[1].nodeID]}
        self.state["edge_states"].append(edge_rep)
    def get_json(self):
        return json.dumps(self.state)

class InitialStateVisitor(visitor):
    def __init__(self):
        super(InitialStateVisitor, self).__init__()
        self.initial_tiles = 19*[None]
        #L-R T-B for drawing purposes
        self.loc_lookup = {
                'A' :0, 'L':1, 'K':2, 'B':3, 'M' : 4, 'R': 5, 'J' : 6,
                'C':7, 'N':8, 'S':9, 'Q':10, 'I':11, 'D':12, 'O':13,
                'P':14, 'H':15, 'E':16, 'F':17, 'G':18
                }
    def get_json(self):
        return json.dumps(self.initial_tiles)
    def visit_tile(self, obj):
        dict_rep = {'id' :obj.tileID, 'resource':obj.resource, 'dienum' : obj.number}
        self.initial_tiles[self.loc_lookup[obj.tileID]] = dict_rep
