from interface import *
import engine
from random import random
from collections import deque
from copy import deepcopy

#Authors: Max Roth (mdr5829), Jacob Welinghoff (jgw7654)

class aSquare(object):
    __slots__ = ('N','S','E','W','RC')
    def __init__(self,N,S,E,W,R,C): [self.N,self.S,self.E,self.W,self.RC] = [N,S,E,W,(R,C)]

class aBoard(object):
    __slots__ = ('data','wallmidpts', 'players', 'me')
    def __init__(self,data,wallmidpts, players, me): [self.data, self.wallmidpts, self.players, self.me] = [data, wallmidpts, players, me]

class Player(object):
    __slots__ = ('location','goals','wallsLeft')
    def __init__(self,location,goals,wallsLeft):
        if goals != None: [self.location, self.goals, self.wallsLeft] = [location,goals,wallsLeft]
        else:
            [self.location,self.wallsLeft] = [location, wallsLeft]
            if location[1] == 4 and location[0] == 8: self.goals=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8)]
            if location[1] == 4 and location[0] == 0: self.goals=[(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)]
            if location[0] == 4 and location[1] == 8: self.goals=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
            if location[0] == 4 and location[1] == 0: self.goals=[(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]

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
    for square in board.data: [square.N,square.S,square.W,square.E] = [board.data[(square.RC[0]-1)*9+square.RC[1]] if square.RC[0] - 1 >= 0 else None,
                                                                       board.data[(square.RC[0]+1)*9+square.RC[1]] if square.RC[0] + 1 < 9 else None,
                                                                       board.data[square.RC[0]*9+square.RC[1]-1] if square.RC[1] - 1 >= 0 else None,
                                                                       board.data[square.RC[0]*9+square.RC[1]+1] if square.RC[1] + 1 < 9 else None]               
    return breakwalls(open(gameFile, 'r').read().split('\n'),board)

def boardtodict(board,dictlist={}):
    for square in board.data: dictlist[square.RC] = [neigh.RC if isinstance(neigh,aSquare) else None for neigh in [square.N,square.S,square.E,square.W]]
    return dictlist

def bfs(boarddict, start):
    queue, enqueued = deque([(None, start)]), set([start])
    while queue:
        parent, n = queue.popleft()
        yield parent, n
        new = set(boarddict[n]) - enqueued
        enqueued |= new
        queue.extend([(n, child) for child in new])

def shortest_path(board, start, end,results=[]):
    if isinstance(end, list):
        for i in end:
            r = shortest_path(board, start, i)
            if isinstance(r, list):
                if len(r) > 0: results += [r]
        if len(results) == 0: return []
        m = results[0]
        for x in range (1, len(results)):
            if len(results[x]) < len(m): m = results[x]
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

def move(playerData):
    if random() >= 0.5 or playerData.players[playerData.me].wallsLeft == 0:
        move = True
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
                    if sq.RC == coor1: playerAsquare = sq
                    if sq.RC == player.location: playerBsquare = sq
                for neighbor in [playerAsquare.N,playerAsquare.S,playerAsquare.E,playerAsquare.W,\
                                 playerBsquare.N,playerBsquare.S,playerBsquare.E,playerBsquare.W]:
                    if isinstance(neighbor,aSquare):
                        occ = False
                        for p in playerData.players:
                            if neighbor.RC == p.location: occ = True
                        if not occ: valid.append(neighbor.RC)
                coor2 = coor1
                minLength = None
                for loc in valid:
                    path = shortest_path(playerData, loc, playerData.players[playerData.me].goals)
                    if path != []:
                        if minLength == None or len(path) < minLength: 
                            coor2 = loc
                            minLength = len(path)                
        playerData.players[playerData.me].location = coor2
    else:
        move = False
        mid = playerData.wallmidpts
        bad = []
        while mid is playerData.wallmidpts or mid in playerData.wallmidpts:
            if len(bad) >= 112:
                move = True
                coor1 = playerData.players[playerData.me].location
                if shortest_path(playerData, coor1, playerData.players[playerData.me].goals) == []: coor2 = coor1, noMove = True
                else: coor2 = shortest_path(playerData, coor1, playerData.players[playerData.me].goals)[1], noMove = False
                for player in playerData.players:
                    if coor2 == player.location and not noMove:
                        valid = []
                        for sq in playerData.data:
                            if sq.RC == coor1: playerAsquare = sq
                            if sq.RC == player.location: playerBsquare = sq
                        print(playerAsquare.RC)
                
                        print(playerBsquare.RC)
                        for neighbor in [playerAsquare.N,playerAsquare.S,playerAsquare.E,playerAsquare.W,\
                                         playerBsquare.N,playerBsquare.S,playerBsquare.E,playerBsquare.W]:
                            if isinstance(neighbor,aSquare):
                                if neighbor.RC != player.location and neighbor.RC != playerData.players[playerData.me].location:valid.append(neighbor.RC)
                        coor2 = coor1, minLength = None
                        for loc in valid:
                            path = shortest_path(playerData, loc, playerData.players[playerData.me].goals)
                            if path != []:
                                if minLength == None or len(path) < minLength: coor2 = loc, minLength = len(path)                
                playerData.players[playerData.me].location = coor2
                return playerData, PlayerMove(playerData.me, move, coor1, coor2)
            cont = True
            coor1 = (int(random() * 9), int(random() * 9))
            roll = int(random() * 4)
            if roll < 2:
                if roll == 0:
                    coor2 = (coor1[0], coor1[1] + 2)
                    if coor2[1] < 9:mid = (coor1[0], coor1[1] + 1)
                    else:cont = False
                else:
                    coor2 = (coor1[0], coor1[1] - 2)
                    if coor2[1] >= 0:mid = (coor1[0], coor1[1] - 1)
                    else:cont = False
            else:
                if roll == 2:
                    coor2 = (coor1[0] + 2, coor1[1])
                    if coor2[0] < 9: mid = (coor1[0] + 1, coor1[1])
                    else: cont = False
                else:
                    coor2 = (coor1[0] - 2, coor1[1])
                    if coor2[0] >= 0: mid = (coor1[0] - 1, coor1[1])
                    else: cont = False
            if mid is not playerData.wallmidpts and cont:
                if coor2[0] < coor1[0] or coor2[1] < coor1[1]: coor1,coor2 = coor2,coor1
                if (coor1[0] == coor2[0] and coor1[0] == 0) or (coor1[1] == coor2[1] and coor1[1] == 0): mid = playerData.wallmidpts
                for i in playerData.wallmidpts:
                    if coor1[0] == coor2[0]:
                        if i[0] == coor1[0]:
                            if i[1] == coor1[1] or i[1] == coor2[1]:
                                if (coor1,coor2) not in bad: bad.append((coor1,coor2))
                                mid = playerData.wallmidpts
                                cont = False
                    else:
                        if i[1] == coor1[1]:
                            if i[0] == coor1[0] or i[0] == coor2[0]:
                                if (coor1,coor2) not in bad:
                                    bad.append((coor1,coor2))
                                mid = playerData.wallmidpts
                                cont = False
            if cont:
                test = deepcopy(playerData)
                breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + str(coor2[0]) + ' ' + str(coor2[1])], test)
                test.players[test.me].wallsLeft -= 1
                test.wallmidpts.append(mid)
                if shortest_path(test, test.players[test.me].location, test.players[test.me].goals) == []:
                    if (coor1,coor2) not in bad: bad.append((coor1,coor2))
                    mid = playerData.wallmidpts
        breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + str(coor2[0]) + ' ' + str(coor2[1])], playerData)
        playerData.players[playerData.me].wallsLeft -= 1
        playerData.wallmidpts.append(mid)
            
         
    return playerData, PlayerMove(playerData.me, move, coor1, coor2)    
    
def last_move(playerData,PlayerMove):
    if PlayerMove.move:
        playerData.players[PlayerMove.playerId].location = PlayerMove.end
    else:
        playerData.players[PlayerMove.playerId].wallsLeft -= 1
        [coor1,coor2]=[PlayerMove.start,PlayerMove.end]
        breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + \
                    str(coor2[0]) + ' ' + str(coor2[1])], playerData)
    return playerData
