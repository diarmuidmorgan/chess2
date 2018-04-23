import gs as gs
from stats import analyze as an
from stats import validCoords
from models import forest
import numpy as np

import pandas as pd
#fi=forest(pikl='data/forestmodelDepth20.pkl')

def mine(row):

    cols = [col for col in 'id,moves_taken_so_far,winner,white_rating,black_rating,opening,victory_type,00,01,02,03,04,05,06,07,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,60,61,62,63,64,65,66,67,70,71,72,73,74,75,76,77,possible_moves,captures,protects,forks,basicScore,pins,centrePawns,pawnsGuardingKings,kingMoves,pawnRanks,fianachettos,checked,pawnLines,stackedPawns,enpassants,canCastle,hasCastled,protectingPieces,backRanks'.split(',')]
    d={}
    keys = [col for col in cols if col not in ['id', 'moves_taken_so_far', 'winner', 'white_rating', 'black_rating', 'opening', 'victory_type']]

    for col in cols:
        d[col]=[]

    i_d = row['id']
    whiteRating = row['white_rating']
    blackRating = row['black_rating']
    winner = row['winner']
    opening_name = row['opening_name']
    moves = row['moves']
    victory_type=row['victory_status']

    results = playGame(moves, winner)
    move=0
    for result in results:
        move+=1
        d['id'].append(i_d)
        d['moves_taken_so_far'].append(move)
        d['white_rating'].append(whiteRating)
        d['black_rating'].append(blackRating)
        d['winner'].append(winner)
        d['victory_type'].append(victory_type)
        d['opening'].append(opening_name)
        for index, cell in enumerate(result):

            d[keys[index]].append(cell)

    return pd.DataFrame.from_dict(d)




def MO(move):
    ''' "preprocesses" moves so they can be interpreted by the game state object'''
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

def playGame(string, winner, printStates=False,printStats=False,wait=False, printPredict=False):

    '''Plays through a game and returns an array of gamestate arrays.
    Optional parameters for printing information and making predictions'''
    global fi
    board = [[5,3,4,1000,9,4,3,5],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,-1,-1,-1,-1,-1,-1,-1],
    [-5,-3,-4,-1000,-9,-4,-3,-5],]
    ep={-1:[], 1:[]}

    canCastle = {1000:{'queen':True, 'king':True}, -1000:{'queen':True, 'king':True}}
    hasCastled = {1000:False, -1000:False}

    color=-1
    ep={-1:[], 1:[]}
    array=[]
    move=0
    for m in string.split(' '):

        if wait:
            i=input('press enter:')
        g=gs.gamestate(board, ep ,canCastle,hasCastled)

        g.getPinnedSquares()
        g.pinPieces()
        g.getAllMoves()

        if move!=0:
            ao=an(state=g)
            ao.analyze()
            arr=ao.produceStateArray()
            array.append(arr)

        if printStates:
            g.representBoard()

        color=color*-1

        new_move=MO(m)

        board=g.moveToInstruction(color,new_move)

        #if printPredict:
            #print('actual winner:', winner)
            #print('Predicted winnger', fi.evaluate(board,move))
        ep=g.enpassants

        canCastle = g.canCastle
        hasCastled = g.hasCastled
        move+=1




    g=gs.gamestate(board, {-1:[], 1:[]},g.canCastle,g.hasCastled)

    g.getPinnedSquares()
    g.pinPieces()
    g.getAllMoves()
    ao=an(state=g)
    ao.analyze()
    arr=ao.produceStateArray()
    array.append(arr)

    return array
if __name__=='__main__':

    playGame('d4 d5 c4 c6 cxd5 e6 dxe6 fxe6 Nf3 Bb4+ Nc3 Ba5 Bf4','black')
