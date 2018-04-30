from flask import render_template
from app import app
import time
from flask import request
import json
import gs
import thinker2
import copy
import time
thinker = thinker2.thinker()
currentArr=json.load(open('data/openings.json'))['games']
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
gamestate = gs.gamestate(board, ep, canCastle, hasCastled)
from flask import request
import json
moveNum=1

#idea is to provide a visual interface with chess.js
@app.route('/')
def index():
    global gamestate
    global moveNum
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
    gamestate = gs.gamestate(board, ep, canCastle, hasCastled)
    '''loads index page'''
    html = open('app/board.html','r').read()
    return html

@app.route('/move')
def move():

    global gamestate
    global moveNum
    global currentArr
    print(len(currentArr))

    FENstring = request.args.get('FEN')
    response = FENtoGS(FENstring, gamestate.board, 1, gamestate.hasCastled, gamestate.canCastle)
    if response == None:
        return json.dumps({'fen':'received'})
    else:
        gamestate=response
    moveNum+=1
    new_board=None
    if len(currentArr)>0:
        found=False

        for index, b in enumerate(currentArr):

            if found==False:
                if b[0]==gamestate.board:

                    currentArr = currentArr[index][1]
                    best_score=-1
                    best_board=[]
                    best_index=0
                    if len(currentArr)>0:

                        for index2, b2 in enumerate(currentArr):

                            if b2[3]>best_score:
                                best_board =b2[0]
                                best_index = index2
                                best_score=b2[3]
                        print('newboad going out')
                        found=True
                        new_board = best_board
                        currentArr = currentArr[best_index][1]
                        time.sleep(0.5)


                    else:
                        new_board = None
                        break
            else:
                break

    if new_board == None:

        new_move = thinker.rootthink(gamestate, -1, moveNum )

        if new_move==[]:
            print('check mate')
            return None
        elif new_move['type']=='castle':
            board=gamestate.castle(-1, abs(new_move['number']))
            gamestate=gamestate.returnNewGameState(board)

        else:
            board=gamestate.simpleMove(1,gamestate.board[new_move['origin'][0]][new_move['origin'][1]], new_move['origin'], new_move['destination'])
            gamestate=gamestate.returnNewGameState(board)
    else:
        gamestate=gamestate.returnNewGameState(new_board)

    moveNum+=1
    return json.dumps({'fen':gsToFen(gamestate)})

def gsToFen(gs):

    board=gs.board
    keys={-5:'r', 5:'R',-1000:'k', 1000:'K', -9:'q',9:'Q',-1:'p', 1:'P', -4:'b', 4:'B', -3:'n', 3:'N'}
    FENstring=''
    for x in range (7, -1, -1):

        numbers=False
        currentNumber=0
        for y in range(7, -1, -1):

            if board[x][y] in keys:
                if currentNumber>0:
                    FENstring+=str(currentNumber)
                FENstring+=keys[board[x][y]]

                currentNumber=0
            elif y == 0:
                currentNumber+=1

                FENstring+=str(currentNumber)

            else:
                currentNumber+=1

        FENstring+='/'

    return FENstring[:-1]




def FENtoGS(FENstring,board, color, hasCastled, canCastle):


    new_board = [[0 for x in range(8)] for y in range(8)]

    keys={'r':-5, 'R':5, 'k':-1000, 'K':1000, 'q':-9, 'Q':9, 'p':-1, 'P':1, 'b':-4, 'B':4, 'n':-3, 'N':3}
    arr = FENstring.split('/')

    ep={-1:[], 1:[]}
    for x in range(7, -1, -1):

        count=0
        for y in range(len(arr[x])-1, -1, -1):

            if arr[x][y] in keys:
                new_board[7-x][count]=keys[arr[x][y]]
                count+=1
            else:
                count+=int(arr[x][y])


    #compare boards
    differences = []
    for x in range(8):

        for y in range(8):

            if board[x][y]!=new_board[x][y]:

                differences.append({'pos':[x,y], 'newValue':new_board[x][y], 'oldValue':board[x][y]})

    if len(differences) == 2:

        for difference in differences:
            if difference['newValue']==0:
                d1=difference
            else:
                d2=difference
        if abs(d1['oldValue'])==1000:
            print('kingmove')
            if abs(d1['pos'][0] - d2['pos'][0]) > 1 or abs(d1['pos'][1]-d2['pos'][1]>0):
                return None


        if color==1 and d2['newValue']==1:
            if d1['pos'][0]==1 and d2['pos'][0]==3:
                ep[1].append(d2['pos'])
        elif color==-1 and d2['newValue']==-1:
            if d1['pos'][0]==6 and d2['pos'][0]==4:
                ep[-1].append(d2['pos'])

        elif abs(d2['newValue'])==1000:

            canCastle[color*1000]['queen']=False
            canCastle[color*1000]['king']=False

        elif abs(d1['oldValue']==5):
            pieceColor = int(d1['oldValue']/abs(d1['oldValue']))
            if d1['pos'] == [0,0]:
                canCastle[pieceColor]['king']=False

            elif d1['pos'] == [7,7]:
                canCastle[pieceColor]['queen']=False

            elif d2['pos']== [7,0]:
                canCastle[pieceColor]['king']=False

            elif d1['pos']== [0,7]:
                canCastle[pieceColor]['queen']=False



        #just check for enpassants if this is the case

    else:
        for difference in differences:

            if difference['pos']==[0, 4]:
                hasCastled[1]=True
            elif difference['pos']==[7,4]:
                hasCastled[-1]=True


    return gs.gamestate(new_board, ep, canCastle, hasCastled)

        #check for castles
