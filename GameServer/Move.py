class Move(object):
    def __init__(self, originator, typ, optiond = None):
        self.typ = typ
        self.playerid = originator
        self.optiond = optiond
        if typ == 'build':
            self.structure = optiond['structure']
            self.location = optiond['location']
        elif typ == 'trade':
            self.target = optiond['target']
            self.offer = optiond['offer']
            self.want = optiond['want']
        elif typ == 'robber':
            self.location = optiond['location']
        elif typ == 'takecard':
            self.target = optiond['target']
        elif typ == 'playcard':
            self.card = optiond['card']
            self.target = optiond['target']
        elif typ == 'discard':
            self.card = optiond['card']
        elif typ == 'endturn':
            pass
        else:
            raise Exception("Invalid move %s" % typ)
    def __repr__(self):
        return "Move(%s,%s, %s)" % (self.typ, self.playerid, str(self.optiond))

    def __str__(self):
        return self.__repr__()

