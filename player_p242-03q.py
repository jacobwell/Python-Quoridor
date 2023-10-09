from interface import *
import engine
from random import random
from collections import deque
from copy import deepcopy

"""
The player module is called by the engine to conduct game play.  You should
not modify the signatures for the init(), shortest_path(), move() 
and last_move() functions.  You are free to implement any other routines or modules.

Author: Max Roth, Jacob Welinghoff
"""

from collections import deque

class aSquare(object):
    __slots__ = ('N','S','E','W','RC')
    def __init__(self,N,S,E,W,R,C): [self.N,self.S,self.E,self.W,self.RC] = [N,S,E,W,(R,C)]

class aBoard(object):
    __slots__ = ('data','wallmidpts', 'players', 'me')
    def __init__(self,data,wallmidpts, players, me):
        [self.data, self.wallmidpts, self.players, self.me] = [data, wallmidpts, players, me]

class Player(object):
    __slots__ = ('location','goals','wallsLeft')
    def __init__(self,location,goals,wallsLeft):
        if goals != None:
            [self.location, self.goals, self.wallsLeft] = [location,goals,wallsLeft]
        else:
            self.location = location
            self.wallsLeft = wallsLeft
            self.goals = []
            if location[1] == 4:
                if location[0] == 8: x = 0
                elif location[0] == 0: x = 8
                for y in range(9):
                    self.goals.append((x,y))
            elif location[0] == 4:
                if location[1] == 8: y = 0
                elif location[1] == 0: y = 8
                for x in range(9):
                    self.goals.append((x,y))

def breakwalls(walls,board):
    for item in walls:
        if item != "":
            [r1,c1,r2,c2] = [int(x) for x in item.split(' ')]
            if r1 == r2: board.data[(r1-1)*9+c1].S = board.data[(r1-1)*9+c1+1].S = board.data[r1*9+c1].N = board.data[r1*9+c1+1].N = 1, board.wallmidpts.append((r1,c1+1))
            else: board.data[r1*9+c1-1].E = board.data[(r1+1)*9+c1-1].E = board.data[r1*9+c1].W = board.data[(r1+1)*9+c1].W = 1, board.wallmidpts.append((r1+1,c1))
    return board

def init(gameFile, playerId, numPlayers, playerHomes, wallsRemaining):
    players = []
    if numPlayers <= 2: w = wallsRemaining[0]
    else: w = wallsRemaining[1]
    for num in range(numPlayers): players += [Player(playerHomes[num],None,w)]                   
    board=aBoard([aSquare(None,None,None,None,num//9, num%9) for num in range(81)],[],players, playerId)
    for square in board.data:
        [square.N,square.S,square.W,square.E] = [board.data[(square.RC[0]-1)*9+square.RC[1]] if square.RC[0] - 1 >= 0 else None,
                                                 board.data[(square.RC[0]+1)*9+square.RC[1]] if square.RC[0] + 1 < 9 else None,
                                                 board.data[square.RC[0]*9+square.RC[1]-1] if square.RC[1] - 1 >= 0 else None,
                                                 board.data[square.RC[0]*9+square.RC[1]+1] if square.RC[1] + 1 < 9 else None]               
    return breakwalls(open(gameFile, 'r').read().split('\n'),board)

def boardtodict(board):
    dictlist = {}
    for square in board.data:
        dictlist[square.RC] = [neigh.RC if isinstance(neigh,aSquare) else None for neigh in [square.N,square.S,square.E,square.W]]
    return dictlist

def bfs(boarddict, start):
    queue, enqueued = deque([(None, start)]), set([start])
    while queue:
        parent, n = queue.popleft()
        yield parent, n
        new = set(boarddict[n]) - enqueued
        enqueued |= new
        queue.extend([(n, child) for child in new])

def shortest_path(board, start, end):
    if isinstance(end, list):
        results = []
        for i in end:
            r = shortest_path(board, start, i)
            if isinstance(r, list):
                if len(r) > 0:
                    results += [r]
        if len(results) == 0:
            return []
        m = results[0]
        for x in range (1, len(results)):
            if len(results[x]) < len(m):
                m = results[x]
        return m
    boarddict = {}
    for square in board.data:
        neighrc = []
        for neigh in [square.N,square.S,square.E,square.W]:
            if isinstance(neigh,aSquare): neighrc.append(neigh.RC)
        boarddict[square.RC] = neighrc
    paths = {None: []}
    for parent, child in bfs(boarddict, start):
        paths[child] = paths[parent] + [child]
        if child == end: return paths[child]
    return None

def makeMove(playerData):
    coor1 = playerData.players[playerData.me].location
    if shortest_path(playerData, coor1, playerData.players[playerData.me].goals) == []:
        coor2 = coor1
        noMove = True
    else:
        coor2 = shortest_path(playerData, coor1, playerData.players[playerData.me].goals)[1] 
        noMove = False
    for player in playerData.players:
        if coor2 == player.location and not noMove:
            valid = []
            for sq in playerData.data:
                if sq.RC == coor1:
                    playerAsquare = sq
                if sq.RC == player.location:
                    playerBsquare = sq
            for neighbor in [playerAsquare.N,playerAsquare.S,playerAsquare.E,playerAsquare.W,\
                             playerBsquare.N,playerBsquare.S,playerBsquare.E,playerBsquare.W]:
                if isinstance(neighbor,aSquare):
                    occ = False
                    for p in playerData.players:
                        if neighbor.RC == p.location:
                            occ = True
                    if not occ:
                        valid.append(neighbor.RC)
            coor2 = coor1
            minLength = None
            for loc in valid:
                path = shortest_path(playerData, loc, playerData.players[playerData.me].goals)
                if path != []:
                    if minLength == None or len(path) < minLength:
                        coor2 = loc
                        minLength = len(path)                
    playerData.players[playerData.me].location = coor2
    return (coor1, coor2)

def move(playerData):
    """
    For parts 2-4 the engine calls this method so the player can make a move.
    When it is the player's turn to move, the engine passes the player
    their player data.  The player makes their move and returns their data
    along with a PlayerMove object that contains information about this move.
        playerData - the player's data
    """

    engine.log_msg("player.move called for player " + str(playerData) + " with " + str(playerData))

    if playerData.players[playerData.me].wallsLeft == 0:
        coors = makeMove(playerData)
        return playerData, PlayerMove(playerData.me, True, coors[0], coors[1])
    else:
        move = False
        mid = playerData.wallmidpts
        bad = []
        good = [] #elements of good -> ((coordinates), mid,
                  #length of opponents path, length of your path)
        while True:
            if len(bad) >= 198:
                if good == []:
                    coors = makeMove(playerData)
                    return playerData, PlayerMove(playerData.me, True, coors[0], coors[1])
                else:
                    coor1 = None
                    coor2 = None
                    for wall in good:
                        if (coor1 == None and coor2 == None) or \
                           wall[3] < mydiff:
                            coor1,coor2 = wall[0]
                            mid = wall[1]
                            if(len(wall) > 3):
                                mydiff = wall[3]
                    breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + \
                                ' ' + str(coor2[0]) + ' ' + \
                                str(coor2[1])], playerData)
                    playerData.players[playerData.me].wallsLeft -= 1
                    playerData.wallmidpts.append(mid)
                    return playerData, PlayerMove(playerData.me, move, \
                                                  coor1, coor2)  
            cont = True
            #Anything situational goes here and sets cont to False
            #and good to [((coor1,coor2), mid)]
            #if nothing situational checks to see if a random wall
            #can cut the opposing player(s) shortest path by a
            #certain amount. not the most time efficient but SHOULD
            #keep under move time limit (20 sec)
            if cont:
                coor1 = (int(random() * 9), int(random() * 9))
                roll = int(random() * 4)
                if roll < 2:
                    if roll == 0:
                        coor2 = (coor1[0], coor1[1] + 2)
                        if coor2[1] < 9:
                            mid = (coor1[0], coor1[1] + 1)
                        else:
                            cont = False
                    else:
                        coor2 = (coor1[0], coor1[1] - 2)
                        if coor2[1] >= 0:
                            mid = (coor1[0], coor1[1] - 1)
                        else:
                            cont = False
                else:
                    if roll == 2:
                        coor2 = (coor1[0] + 2, coor1[1])
                        if coor2[0] < 9:
                            mid = (coor1[0] + 1, coor1[1])
                        else:
                            cont = False
                    else:
                        coor2 = (coor1[0] - 2, coor1[1])
                        if coor2[0] >= 0:
                            mid = (coor1[0] - 1, coor1[1])
                        else:
                            cont = False
            if coor2[0] < coor1[0] or coor2[1] < coor1[1]:
                coor1,coor2 = coor2,coor1
            if mid is not playerData.wallmidpts and cont and \
               (coor1, coor2) not in bad:
                if (coor1[0] == coor2[0] and coor1[0] == 0) or \
                   (coor1[1] == coor2[1] and coor1[1] == 0):
                    cont = False
                if cont:
                    for i in playerData.wallmidpts:
                        if coor1[0] == coor2[0]:
                            if i[0] == coor1[0]:
                                if i[1] == coor1[1] or i[1] == coor2[1] or \
                                   i[1] == (coor1[1] + coor2[1]) / 2:
                                    if (coor1,coor2) not in bad:
                                        bad.append((coor1,coor2))
                                    cont = False
                        else:
                            if i[1] == coor1[1]:
                                if i[0] == coor1[0] or i[0] == coor2[0] or \
                                   i[0] == (coor1[0] + coor2[0]) / 2:
                                    if (coor1,coor2) not in bad:
                                        bad.append((coor1,coor2))
                                    cont = False
            if cont and (coor1, coor2) not in bad:
                test = deepcopy(playerData)
                breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + \
                            str(coor2[0]) + ' ' + str(coor2[1])], test)
                test.players[test.me].wallsLeft -= 1
                test.wallmidpts.append(mid)
                for player in test.players:
                    if shortest_path(test, player.location, player.goals) == []:
                        if (coor1,coor2) not in bad:
                            bad.append((coor1,coor2))
                        mid = playerData.wallmidpts
                        cont = False
                if cont:
                    for iD in range(len(test.players)):
                        if iD != test.me:
                            diff = len(shortest_path(test, test.players[iD].location, \
                                                     test.players[iD].goals)) - \
                                   len(shortest_path(playerData, \
                                                     playerData.players[iD].location, \
                                                     playerData.players[iD].goals))
                            mydiff = len(shortest_path(test, \
                                                       test.players[test.me].location, \
                                                       test.players[test.me].goals)) - \
                                     len(shortest_path(playerData, \
                                                       playerData.players[playerData.me].location, \
                                                       playerData.players[playerData.me].goals))
                            if (good == [] and diff >= 2) or \
                               (len(good) > 0 and diff > good[0][2]):
                                good = [((coor1,coor2), mid, diff, mydiff)]
                            elif len(good) > 0 and diff == good[0][2]:
                                wall = ((coor1,coor2), mid, diff, mydiff)
                                if wall not in good:
                                    good.append(wall)
            if (coor1,coor2) not in bad:
                bad.append((coor1,coor2))
            mid = playerData.wallmidpts
            #print(str(diff) + " " + str(len(bad)))
    
def last_move(playerData,PlayerMove):
    if PlayerMove.move:
        playerData.players[PlayerMove.playerId].location = PlayerMove.end
    else:
        playerData.players[PlayerMove.playerId].wallsLeft -= 1
        [coor1,coor2]=[PlayerMove.start,PlayerMove.end]
        breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + \
                    str(coor2[0]) + ' ' + str(coor2[1])], playerData)
    return playerData
