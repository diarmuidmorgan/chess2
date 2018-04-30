example='d4 d5 g3 g6 b3 Bg7 Bb2 Nf6 Bg2 O-O Nf3 Nc6 O-O e6 Ne5 Nxe5 dxe5 Nd7 f4 c6 e4 Qb6+ Bd4 Qc7 exd5 cxd5 Nc3 b6 Nb5 Qd8 Nd6 Ba6 c4 dxc4 bxc4 Rb8 Qa4 Bc8 Qxa7 Bb7 Bxb7 Rxb7 Qxb7 f6 Bxb6 Nxb6 Rab1 Nxc4 Nxc4 Qd4+ Kg2 Qxc4 a3 fxe5 fxe5 Bxe5 Rxf8+ Kxf8 Rf1+ Kg8 Qf7+ Kh8 Qf8#'

#trying to stream line and tidy up the awful process of reading moves contained in run_gamestring
import gs as gs
from stats import analyze as an
from stats import validCoords
from models import forest
import numpy as np
fi=forest(pikl='data/forestmodelDepth20.pkl')

def MO(move):
    print(move)
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

def playGame(string, winner):
    global fi
    board = [[5,3,4,1000,9,4,3,5],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,-1,-1,-1,-1,-1,-1,-1],
    [-5,-3,-4,-1000,-9,-4,-3,-5],]

    color=-1
    ep={-1:[], 1:[]}
    array=[]
    move=0
    canCastle = {1000:{'queen':True, 'king':True}, -1000:{'queen':True, 'king':True}}
    hasCastled = {1000:False, -1000:False}
    for m in string.split(' '):
        print(m)
        i=input('press enter:')
        print('canCastle at miner level: ', canCastle)
        print('making new game state')
        g=gs.gamestate(board, ep ,canCastle,hasCastled)
        g.getPinnedSquares()
        g.pinPieces()
        g.getAllMoves()
        g.representBoard()
        print(g.castles)

        color=color*-1

        new_move=MO(m)
        board=g.moveToInstruction(color,new_move)
        print('actual winner:', winner)
        print('Predicted winner', fi.evaluate(board,move))
        ep=g.enpassants
        canCastle = g.canCastle
        hasCastled = g.hasCastled

        ao=an(g)
        ao.analyze()
        arr=ao.produceStateArray()
        array.append(arr)



    return array

def appendToCsv(fileName, data, baseFeatures,gameNumber):
    count=0
    f=open('data/'+fileName+'.csv', 'a')
    for row in data:
        count+=1
        string=str(gameNumber)+','+str(count)+','
        for feature in baseFeatures:
            string+=str(feature)+','
        try:
            for feature in row:
                string+=str(feature)+','
        except:
            print(row)

        string=string[:-1]+'\n'
        f.write(string)

    f.close()







if __name__ == '__main__':

    data = open('data/games.csv', 'r').read()
    data=data.split('\n')
    errors=0
    if data[-1]=='':
        data=data[0:-1]

    data=data[1:]
    filename='minedgames'
    f=open('data/minedgames.csv','w')
    f.write('gameNumber,move,winner,whiteRating,blackRating,opening,victory_type,00,01,02,03,04,05,06,07,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,60,61,62,63,64,65,66,67,70,71,72,73,74,75,76,77,moves,captures,protects,forks,basicScore,pins,centrePawns,pawnsGuardingKings,kingMoves,pawnRanks,fianachettos,checked,centrePawns,hasCastled,enpassants,\n')
    f.close()

    gameNumber=1
    fCount =0
    t=1
    for line in data:
        fCount+=1
        if fCount >1000:
            fCount=0
            filename='minedgames'+str(t)
            t+=1
            f=open('data/'+filename+'.csv','w')
            f.write('gameNumber,move,winner,whiteRating,blackRating,opening,victory_type,00,01,02,03,04,05,06,07,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,47,50,51,52,53,54,55,56,57,60,61,62,63,64,65,66,67,70,71,72,73,74,75,76,77,moves,captures,protects,forks,basicScore,pins,centrePawns,pawnsGuardingKings,kingMoves,pawnRanks,fianachettos,checked,centrePawns,hasCastled,enpassants,\n')
            f.close()




        gameNumber+=1
        line=line.split(',')
        winner = line[6]
        whiteRating = line[9]
        blackRating = line[11]
        gamestring = line[12]

        opening = line[14]
        victory_type = line[5]
        baseFeatures=[winner,whiteRating,blackRating,opening,victory_type]

        arr=playGame(gamestring, winner)

        appendToCsv(filename,arr,baseFeatures,gameNumber)
