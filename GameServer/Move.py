class Move(object):
    def __init__(self, typ, optiond = None):
        self.typ = typ
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
        elif typ == 'endturn':
            pass
        elif:
            raise Exception("Invalid move %s" % typ)
    def __repr__(self):
        return "Move(%s,%s)" % (self.typ, str(self.optiond))
