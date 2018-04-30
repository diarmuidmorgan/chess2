from gs import gamestate
import copy
from models import forest
forestmodel =forest(pikl='data/fullforest.pikl')
from stats import analyze as an
from stats import validCoords
from models import forest
import numpy as np
from simple_search import rootNode

def MO(move):

    places=['a','b','c','d','e','f','g']
    rows={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7}
    pieces=['N','K','B','R','Q']
    cols = {'a':7, 'b': 6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
    pieces = {'N':3, 'B':4, 'Q':9, 'K':1000, 'R':5}
    move=list(move)
    new_move = {'cols':[], 'rows':[], 'piece':[], 'type':'', 'castles':[]}

    for key in list(move):

        if key in rows:

            new_move['rows'].append(rows[key])

        elif key in cols:

            new_move['cols'].append(cols[key])

        elif key in pieces:

            new_move['piece'].append(pieces[key])



        elif key=='=':

            new_move['type']='promote'



        elif key=='O':

            new_move['castles'].append('O')
            new_move['type']='castle'


    return new_move

color=-1
moveNumber=0
ep={-1:[], 1:[]}
array=[]
move=0
canCastle = {1000:{'queen':True, 'king':True}, -1000:{'queen':True, 'king':True}}
hasCastled = {1000:False, -1000:False}
board = [[5,3,4,1000,9,4,3,5],
[1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[-1,-1,-1,-1,-1,-1,-1,-1],
[-5,-3,-4,-1000,-9,-4,-3,-5],]
while True:

    moveNumber+=1
    color=color*-1
    g=gamestate(board, ep, canCastle, hasCastled)
    g.getPinnedSquares()
    g.pinPieces()
    g.getAllMoves()
    g.representBoard()
    print(g.castles)
    b=copy.copy(g.board[:])
    print(b)
    node1 = rootNode(g, moveNumber, forestmodel)
    new_move = node1.search(color)
    print(new_move)
    origin=new_move['origin']
    destination = new_move['destination']
    b[destination[0]][destination[1]]=b[origin[0]][origin[1]]
    b[origin[0]][origin[1]]=0
    print(b)
    board = b[:]
    color=color*-1
    moveNumber+=1

    found=False
    g=gamestate(board[:], g.enpassants, g.canCastle, g.hasCastled)

    g.getPinnedSquares()
    g.pinPieces()
    g.getAllMoves()
    g.representBoard()
    #etc...
    while not found:
        move = input('please enter a move:')
        move = MO(move)
        board = g.moveToInstruction(color,move)
        if board == None:
            print('that was an invalid move. Try again')

        else:
            found = True
