#Author: Jacob Welinghoff, Max Roth
from interface import *
from random import random
from collections import deque
from copy import deepcopy







def boardtodict(board):
    dictlist = {}
    for square in board.data:dictlist[square.RC] = [neigh.RC if isinstance(neigh,aSquare) else None for neigh in [square.N,square.S,square.E,square.W]]
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
                if len(r) > 0:results += [r]
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
        coor2 = shortest_path(playerData, coor1, playerData.players[playerData.me].goals)[1]
        for player in playerData.players:
            if coor2 == player.location: 
                square=playerData.data[coor2[1]*9+coor2[0]]
                newpath='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                adjacents = [square.N,square.E,square.S,square.W]
                for square in adjacents:
                    if isinstance(square,aSquare):
                        temppath = shortest_path(playerData,square.RC,playerData.players[playerData.me].goals)
                        print("Current len of shortest path: ", len(newpath))
                        print("Current len of temp path: ", len(temppath))
                        if len(temppath) <= len(newpath): newpath=temppath
                coor2=newpath[0]
        playerData.players[playerData.me].location = coor2
    else:
        move = False
        mid = playerData.wallmidpts
        bad = []
        while mid is playerData.wallmidpts or mid in playerData.wallmidpts:
            if len(bad) >= 112:
                move = True
                coor1 = playerData.players[playerData.me].location
                coor2 = shortest_path(playerData, coor1, playerData.players[playerData.me].goals)[1] 
                playerData.players[playerData.me].location = coor2
                return playerData, PlayerMove(playerData.me, move, coor1, coor2)
            cont = True
            coor1 = (int(random() * 9), int(random() * 9))
            roll = int(random() * 4)
            if roll < 2:
                if roll == 0:
                    coor2 = (coor1[0], coor1[1] + 2)
                    if coor2[1] < 9: mid = (coor1[0], coor1[1] + 1)
                    else: cont = False
                else:
                    coor2 = (coor1[0], coor1[1] - 2)
                    if coor2[1] >= 0: mid = (coor1[0], coor1[1] - 1)
                    else:cont = False
            else:
                if roll == 2:
                    coor2 = (coor1[0] + 2, coor1[1])
                    if coor2[0] < 9:mid = (coor1[0] + 1, coor1[1])
                    else: cont = False
                else:
                    coor2 = (coor1[0] - 2, coor1[1])
                    if coor2[0] >= 0: mid = (coor1[0] - 1, coor1[1])
                    else: cont = False
            if mid is not playerData.wallmidpts and cont:
                if coor2[0] < coor1[0] or coor2[1] < coor1[1]: coor1,coor2 = coor2,coor1
                if (coor1[0] == coor2[0] and coor1[0] == 0) or \
                   (coor1[1] == coor2[1] and coor1[1] == 0): mid = playerData.wallmidpts
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
                                if (coor1,coor2) not in bad: bad.append((coor1,coor2))
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
    if PlayerMove.move: playerData.players[PlayerMove.playerId].location = PlayerMove.end
    else:
        playerData.players[PlayerMove.playerId].wallsLeft -= 1
        [coor1,coor2]=[PlayerMove.start,PlayerMove.end]
        breakwalls([str(coor1[0]) + ' ' + str(coor1[1]) + ' ' + \
                    str(coor2[0]) + ' ' + str(coor2[1])], playerData)
    return playerData