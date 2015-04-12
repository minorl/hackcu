from random import shuffle
import copy

class GameBoard(object):
    def __init__(self):
        self.corners = []
        self.edges = {} #(id1,id2)->CornerEdge
        self.tiles = {}
        self.buildingCounts = {'road':[0,0,0,0],'settlement':[0,0,0,0],'city':[0,0,0,0]} #building->[p1,p2,p3]
        self.possibleTiles = ['desert','ore','ore','ore','wood','wood','wood','wood','brick','brick','brick','sheep','sheep','sheep','sheep','wheat','wheat','wheat','wheat']
        self.harvestNumber = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
        shuffle(self.possibleTiles)
        self.cornerTbl = {0:(1,8,None),1:(None,2,0),2:(3,10,1),3:(None,4,2),4:(5,12,3),5:(None,6,4),6:(None,14,5),
        7:(8,17,None),8:(0,9,7),9:(10,19,8),10:(11,2,9),11:(12,21,10),12:(4,13,11),13:(14,23,12),14:(6,15,13),15:(None,25,14),
        16:(17,27,None),17:(7,18,16),18:(19,29,17),19:(9,20,18),20:(21,31,19),21:(11,22,20),22:(23,33,21),23:(13,24,22),24:(25,35,23),25:(15,26,24),26:(None,37,25),
        27:(16,28,None),28:(29,38,27),29:(18,30,28),30:(31,40,29),31:(20,32,30),32:(33,42,31),33:(22,34,32),34:(35,44,33),35:(24,36,34),36:(37,46,35),37:(26,None,36),
        38:(28,39,None),39:(40,47,38),40:(30,41,39),41:(42,49,40),42:(32,43,41),43:(44,51,42),44:(34,45,43),45:(46,53,44),46:(36,None,45),
        47:(39,48,None),48:(49,None,47),49:(41,50,48),50:(51,None,49),51:(43,52,50),52:(53,None,51),53:(45,None,52)}
        self.tileTbl = {'A':(1,2,10,9,8,0),
                        'B':(8,9,19,18,17,7),
                        'C':(17,18,29,28,27,16),
                        'D':(29,30,40,39,38,28),
                        'E':(40,41,49,48,47,39),
                        'F':(42,43,51,50,49,41),
                        'G':(44,45,53,52,51,43),
                        'H':(35,36,46,45,44,34),
                        'I':(25,26,37,36,35,24),
                        'J':(14,25,35,24,23,13),
                        'K':(5,6,14,13,12,4),
                        'L':(3,4,12,11,10,2),
                        'M':(10,11,21,20,19,9),
                        'N':(19,20,31,30,29,18),
                        'O':(31,32,42,41,40,30),
                        'P':(33,34,44,43,42,32),
                        'Q':(23,24,35,34,33,22),
                        'R':(12,13,23,22,21,11),
                        'S':(21,22,33,32,31,20)}
        self.robberPos = None


        self.createCorners()
        self.createEdges()
        self.createTiles()
        #print self.robberPos
        #print [str(corner) for corner in self.corners] 
    def createCorners(self):
        for i in range(54):
            newCorner = Corner(i)
            self.corners.append(newCorner)
        
    def createEdges(self):
        for i in range(54):
            startCorner = self.corners[i]
            for item in range(3):
                j= self.cornerTbl[i][item]
                if j == None:
                    continue
                endCorner = self.corners[j]
                key = tuple(sorted((i,j)))
                if not self.edges.has_key(key):
                    newEdge = CornerEdge(startCorner,endCorner)
                    self.edges[key] = newEdge
                    startCorner.addEdge(newEdge)
                    endCorner.addEdge(newEdge)
    def createTiles(self):
        #print self.possibleTiles
        harvestNum =0
        for i in range(19):
            curChar = unichr(65+i)
            if self.possibleTiles[i]== 'desert':
                newTile = Tile(curChar, self.possibleTiles[i],None)
                self.robberPos = curChar
            else:
                newTile = Tile(curChar, self.possibleTiles[i],self.harvestNumber[harvestNum])
                harvestNum+=1
            self.tiles[curChar]= newTile
            for j in range(6):
                self.corners[self.tileTbl[curChar][j]].addTile(newTile)
    def addRoad(self,corner1ID,corner2ID, playerID):
        self.buildingCounts["road"][playerID]+=1
        key = tuple(sorted((corner1ID,corner2ID)))
        self.edges[key].addRoad(playerID)
    def addBuilding(self,cornerID,playerID,buildingTag):
        if buildingTag == "settlement":
            self.buildingCounts[buildingTag][playerID]+=1
        if buildingTag == "city":
            self.buildingCounts["settlement"][playerID]-=1
            self.buildingCounts[buildingTag][playerID]+=1
        self.corners[cornerID].addBuilding(playerID,buildingTag)

    def getEdge(self, corner1ID,corner2ID):
        key = tuple(sorted((corner1ID,corner2ID)))
        return self.edges[key]
    def hasColorRoad(self, cornerID, playerID):
        for road in self.corners[cornerID].edges:
            if road.playerID== playerID:
                return True
        return False

    def getBuildings(self,dieRoll):
        settlements=[]
        # location = self.harvestNumber[dieRoll]
        for t in self.tiles.itervalues():
            if t.number == dieRoll:
                for cornerID in self.tileTbl[t.tileID]:
                    corner = self.corners[cornerID]
                    if corner.buildingPlayerID!=None:
                        settlements.append((t.resource, corner.buildingPlayerID,corner.buildingTag))
        return settlements

    def getCount(self,playerID,buildingTag):
        return self.buildingCounts[buildingTag][playerID]
    def getCounts(self,buildingTag):
        return self.buildingCounts[buildingTag]
    def accept(self,v):
        v.visit(self)
        for c in self.corners:
            c.accept(v)
        for t in self.tiles.itervalues():
            t.accept(v)
        for e in self.edges.itervalues():
            e.accept(v)

    def getRobberPos(self):
        return self.robberPos

    def getLongestRoad(self):
        playerRoads = [0,0,0,0]
        for c in self.corners:
            visitedCorners = []
            startCorner = c
            roadLength = 0
            for i in range(4):
                curDist = self.recurseRoad(c, 0, visitedCorners, i)
                if curDist >playerRoads[i]:
                    playerRoads[i]=curDist
        print playerRoads
            
                #print road
    def recurseRoad(self,c,dist, visitedCorners, playerID):
        visitedCorners = copy.copy(visitedCorners)
        visitedCorners.append(c)
        maxDist =dist
        for road in c.edges:
            if road.hasRoad:
                if road.playerID!= playerID:
                    continue

                corner1 = road.corners[0]
                corner2 = road.corners[1]
                nextCorner = corner2 if c is corner1 else corner1
                if nextCorner.buildingPlayerID!= None and nextCorner.buildingPlayerID!=playerID:
                    curDist= dist+1
                    if curDist>maxDist:
                        maxDist = curDist
                elif not nextCorner in visitedCorners:
                    curDist =self.recurseRoad(nextCorner,dist+1,visitedCorners, playerID)
                    if curDist>maxDist:
                        maxDist = curDist
        return maxDist



        



class Corner(object):
    def __init__(self,nodeID):
        self.nodeID = nodeID
        self.edges = []
        self.tiles = []
        self.buildingTag = None
        self.buildingPlayerID = None
    def __str__(self):
        return "ID: %d,%s"% (self.nodeID,[str(tile) for tile in self.tiles])
    def addEdge(self, edge):
        self.edges.append(edge)
    def addTile(self,tile):
        self.tiles.append(tile)
        if len(self.tiles)>3:
            del self.tiles[0]

    def addBuilding(self,playerID, buildingTag):
        self.buildingTag=buildingTag
        self.buildingPlayerID=playerID
    def accept(self, v):
        v.visit(self)


class Tile(object):
    def __init__(self,tileID, resource,number):
        self.tileID = tileID
        self.resource = resource
        self.number = number
    def __str__(self):
        return "Tile %s, %s,Freq %s"%(self.tileID, self.resource,self.number)
    def accept(self,v):
        v.visit(self)

class CornerEdge(object):
    def __init__(self,corner1, corner2):
        self.hasRoad = False
        self.corners = (corner1, corner2)
        self.playerID = None
    def addRoad(self, playerID):
        self.hasRoad = True
        self.playerID = playerID
    def accept(self,v):
        v.visit(self)
    def __str__(self):
        return "Road (%d,%d),%s"%(self.corners[0].nodeID,self.corners[1].nodeID,self.playerID)

#board = GameBoard()
#board.addRoad(0,1,3)
#board.addBuilding(0,3,"settlement")
#board.getLongestRoad()