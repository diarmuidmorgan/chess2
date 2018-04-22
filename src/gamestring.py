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

    color=-1
    ep={-1:[], 1:[]}
    array=[]
    move=0
    for m in string.split(' '):
        print(m)
        if wait:
            i=input('press enter:')
        g=gs.gamestate(board, ep ,[],[])
        g.getPinnedSquares()
        g.pinPieces()
        g.getAllMoves()
        if printStates:
            g.representBoard()

        color=color*-1

        new_move=MO(m)
        board=g.moveToInstruction(color,new_move)

        if printPredict:
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
if __name__=='__main__':

    playGame('black','d4 d5 c4 c6 cxd5 e6 dxe6 fxe6 Nf3 Bb4+ Nc3 Ba5 Bf4')
