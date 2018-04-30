import gs as gs
from stats import analyze as an
from stats import validCoords

import numpy as np

class gamereader():

    def __init__(self):
        self.places=['a','b','c','d','e','f','g']
        self.rows={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7}
        self.pieces=['N','K','B','R','Q']
        self.cols = {'a':7, 'b': 6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
        self.pieces = {'N':3, 'B':4, 'Q':9, 'K':1000, 'R':5}


    def MO(self,move):
        '''read a move in chess notation, and create an object that the gamestate object can understand'''

        move=list(move)
        new_move = {'cols':[], 'rows':[], 'piece':[], 'type':'', 'castles':[]}

        for key in list(move):

            if key in self.rows:

                new_move['rows'].append(self.rows[key])

            elif key in self.cols:

                new_move['cols'].append(self.cols[key])

            elif key in self.pieces:

                new_move['piece'].append(self.pieces[key])



            elif key=='=':

                new_move['type']='promote'



            elif key=='O':

                new_move['castles'].append('O')
                new_move['type']='castle'


        return new_move

    def playGameFromString(self,string, winner, print_positions=False, lineByLine=False):
        global fi
        self.board = [[5,3,4,1000,9,4,3,5],
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
        for m in string.split(' '):
            print(m)
            i=input('press enter:')
            g=gs.gamestate(board, ep ,[],[])
            g.getPinnedSquares()
            g.pinPieces()
            g.getAllMoves()
            g.representBoard()

            color=color*-1

            new_move=MO(m)
            board=g.moveToInstruction(color,new_move)
            print('actual winner:', winner)
            print('Predicted winner', fi.evaluate(board,move))
            ep=g.enpassants

            ao=an(g)
            ao.analyze()
            arr=ao.produceStateArray()
            array.append(arr)

        g=gs.gamestate(board, {-1:[], 1:[]},[],[])

        g.getPinnedSquares()
        g.pinPieces()
        g.getAllMoves()

        return array

    def appendToCsv(self,fileName, data, baseFeatures,gameNumber):
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

    def loadGame(self, array):
