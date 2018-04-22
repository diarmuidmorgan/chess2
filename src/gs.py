from pieces.vc import validCoords
from pieces import pawn, king, queen, bishop, knight, rook
import copy


values = {'PAWN':1, 'KNIGHT':3, 'BISHOP':4, 'ROOK':5, 'QUEEN':9, 'KING':1000}

class gamestate():


    def __init__ (self, board, enpassants, canCastle, hasCastled):

        #enpassants, canCastle, and has already castled need to be carried on from the previous gamestate
        pieces = {'PAWN':8, 'ROOK': 2, 'KNIGHT':2, 'BISHOP':2, 'KING':1, 'QUEEN':1}
        self.board = board



        #enpassants, canCastle, and has already castled need to be carried on from the previous gamestate

        self.enpassants = enpassants
        self.canCastle = canCastle
        self.hasCastled = hasCastled
        self.enpassantDestinations = []
        self.pawn=pawn.pawn(pieces)
        self.king=king.king(pieces)
        self.bishop=bishop.bishop(pieces)
        self.knight=knight.knight(pieces)
        self.rook=rook.rook(pieces)
        self.queen=queen.queen(pieces)
        self.collection = self.makeCollection()
        #as both kings can't simultaneously be in check,
        #this will be either -1, 0, or 1
        self.checked = 0
        self.castles = {1000:[],-1000:[]}

    def makeCollection(self):
        board = self.board
        '''basically just make a dictionary of pieces on the board'''
        #positive/negative values represent who owns the piece
        collection = {1:[],-1:[],3:[],-3:[],4:[],-4:[],5:[],-5:[],9:[],-9:[],1000:[],-1000:[]}

        for x, row in enumerate(board):

            for y, piece in enumerate(row):
                if piece!=0:

                    collection[piece].append({'pos':[x,y], 'moves':[], 'captures':[], 'pin':None})

        if board[0][0] != 5:
            self.canCastle[1000]['king']=False

        if board[7][7] != -5:
            self.canCastle[-1000]['queen']=False

        if board[0][7] != 5:
            self.canCastle[1000]['queen']=False

        if board[7][0] != -5:
            self.canCastle[-1000]['king']=False




        return collection

    def scoreMaterial(self):
        #add up and return a sum of all material on the board
        '''score can be either negative or positive, reflecting who is winning'''
        score = 0
        for piece in self.collection:

            score += piece*len(self.collection[piece])

        return score

    def representBoardOld(self):
        '''prints a visual represenation of the board'''
        #the representation is upside down

        board = self.board
        keys = {0:'_', 1:'P', 3:'N',4:'B',5:'R',9:'Q', 1000:'K'}

        string='   '
        for i in range(8):
            string += ' ' + str(i) + ' '
        print(string)

        for x in range(len(board)):
            string = ' '+str(x)+' '
            for y in range(len(board[x])):

                if board[x][y]>0:

                    string += ' '+keys[board[x][y]]+ ' '
                else:
                    string += ' '+keys[abs(board[x][y])].lower() + ' '

            print(string)


    def representBoard(self):
        '''prints a visual represenation of the board'''
        #the representation is upside down
        string = '       A    B    C    D    E    F    G    H    '
        board = self.board
        keys = {0:'_', 1:'P', 3:'N',4:'B',5:'R',9:'Q', 1000:'K'}




        for x in range(len(board)-1,-1,-1):

            string += '\n\n\n  '+str(x+1)+'  '
            for y in range(len(board[x])-1,-1,-1):

                if board[x][y]>0:

                    string += '  '+keys[board[x][y]]+ '  '
                else:
                    string += '  '+keys[abs(board[x][y])].lower() + '  '

        print(string)

    def getPinnedSquares(self):
        #use the king object to return the squares of the board that are pinned, and the directions in which their movement isn't constricted
        board = self.board
        self.pinnedSquares = {1000:[], -1000:[]}

        for piece in self.pinnedSquares:

            x=self.collection[piece][0]['pos'][0]
            y=self.collection[piece][0]['pos'][1]
            color = int(piece/abs(piece))
            self.pinnedSquares[piece]=self.king.returnPins(x,y,color,board)

    def pinPieces(self):
        #add a 'pin' object to any pieces who reside on a pinned square
        for pieceType in self.collection:

            for index in range(0, len(self.collection[pieceType])):

                piece = self.collection[pieceType][index]
                color = int(pieceType/abs(pieceType))

                #positions are hashed for quick look up
                pos = str(piece['pos'][0]) + str(piece['pos'][1])

                if pos in self.pinnedSquares[color*1000]:


                    self.collection[pieceType][index]['pin']=self.pinnedSquares[color*1000][pos]

    def getAllMoves(self):
        #horrible method for finding all checks, all captures, all valid moves etc..
        board = self.board
        self.moves = {1:[], -1:[]}
        self.captures = {1:[], -1:[]}
        self.protects = {1:[], -1:[]}
        self.checks = {1:[], -1:[]}

        for pieceType in self.collection:

            for i in range(0, len(self.collection[pieceType])):

                color = int(pieceType/abs(pieceType))
                pin = self.collection[pieceType][i]['pin']
                x = self.collection[pieceType][i]['pos'][0]
                y = self.collection[pieceType][i]['pos'][1]
                found=False
                if abs(pieceType) == 1:

                    found=True
                    moves = self.pawn.returnValidMoves(x, y,color,board, self.enpassants[color*-1],pin)
                    self.checks[color] += moves['checked']
                    self.checks[color]+=moves['captures']
                    #the squares checked by the pawn must be added seperately, because they are not actually valid moves that the pawn can move into
                elif abs(pieceType)==3:

                    found=True
                    moves = self.knight.returnValidMoves(x, y,color,board,pin)

                elif abs(pieceType)==4:

                    found=True
                    moves = self.bishop.returnValidMoves(x, y,color,board,pin)

                elif abs(pieceType)==5:

                    found=True
                    moves = self.rook.returnValidMoves(x, y,color,board,pin)

                elif abs(pieceType)==9:

                    found=True
                    moves = self.queen.returnValidMoves(x, y,color,board,pin)



                if found:
                    if abs(pieceType)!=1:
                    #if the piece isn't a pawn, all of its valid moves that aren't already captures or protects, are squares that are checked (and the king can't move there)
                        self.checks[color] += moves['moves']
                        self.checks[color] += moves['captures']
                    else:
                        #add enpassant squares that the pawn can capture to it's 'ep' moves
                        self.collection[pieceType][i]['ep']=moves['ep']
                        self.enpassantDestinations += [{'origin':[x,y], 'destination':coords} for coords in moves['ep']]
                    #add all valid moves, captures and protects
                    self.moves[color] += [{'origin': [x,y], 'destination': coords} for coords in moves['moves']]
                    self.captures[color] += [{'origin': [x,y], 'destination': coords} for coords in moves['captures']]
                    self.protects[color] += moves['protects']
                    self.collection[pieceType][i]['moves']=moves['moves']
                    self.collection[pieceType][i]['captures']=moves['captures']


        #now do the kings. We know what squares have been checked and made invalid
        for piece in [1000, -1000]:


            color = int(piece/abs(piece))
            x=self.collection[piece][0]['pos'][0]
            y=self.collection[piece][0]['pos'][1]
            moves = self.king.returnValidMoves(x, y, color,board, self.checks[color*-1])

            self.moves[color] += [{'origin': [x,y], 'destination': coords} for coords in moves['moves']]
            self.checks[color] += moves['moves']
            self.captures[color] += [{'origin': [x,y], 'destination': coords} for coords in moves['captures']]
            self.protects[color] += moves['protects']
            self.collection[piece][0]['moves']=moves['moves']
            self.collection[piece][0]['captures']=moves['captures']
            self.collection[piece][0]['protects']=moves['protects']



            if self.king.isChecked(x, y, self.checks[color*-1]):

                self.checked+=color
            #add method to check castling

            #changed code here to add method for castling
            castles = {'king':False, 'queen':False}
            if color==-1:
                rank=7
            else:
                rank = 0


            if self.canCastle[piece]['king']==True:

                if sum(board[rank][1:3])==0:
                    castles['king']=True

            if self.canCastle[piece]['queen']==True:

                if sum(board[rank][4:7])==0:
                    castles['queen']=True

            self.collection[piece][0]['castles'] = castles
            self.castles[color*1000]=castles

    def returnNewGameState(self, board):
        #create a new gamestate object from the current gamestate
        #method currently unused
        return gamestate(board, copy.deepcopy(copy.copy(self.enpassants)),copy.deepcopy(self.canCastle), copy.deepcopy(self.hasCastled) )

#searching for pieces to move
    def searchPieceMove(self, color, piece, destination, col=None,row=None):
        #search for a pice fitting the above criteria that can move to the given destination
        #return it's board position
        if col==None and row == None:

            for p in self.collection[color*piece]:

                if destination in p['moves'] or destination in p['captures']:

                    return p['pos']

        elif col!=None and row == None:

            for p in self.collection[color*piece]:

                if p['pos'][1]==col and (destination in p['moves'] or destination in p['captures']):

                    return p['pos']

        elif col == None and row != None:

            for p in self.collection[color*piece]:

                if p['pos'][0]==row and (destination in p['moves'] or destination in p['captures']):

                    return p['pos']

    def searchPawnMove(self, color, col, typ, number=None, destination=None):
        #search for a pawn that fits the above criteria, and return it's position
        self.enpassants={-1:[], 1:[]}
        if typ == 'capture':

            for p in self.collection[color*1]:

                if p['pos'][1]==col and destination in p['captures']:

                    return {'type':'normalCapture', 'pos':p['pos']}

                elif p['pos'][1]==col and destination in p['ep']:

                    return {'type':'epCapture', 'pos':p['pos']}

        elif typ == 'forward':

            for p in self.collection[color*1]:

                if p['pos'][1]==col and [number, col] in p['moves']:

                    return {'type':'fwd', 'pos':p['pos']}

    def castle(self,color, number):
        self.enpassants={-1:[], 1:[]}
        self.hasCastled[color*1000]=True
        #only if castling is viable. Too lazy to check for that now
        #don't wanna mutate the board
        board = copy.deepcopy(self.board[:])
        if number == 2:
            direction = 'king'
        else:
            direction = 'queen'
        if color == -1:

            if direction == 'king':

                board[7][3]=0
                board[7][0]=0
                board[7][1]=1000*color
                board[7][2]=5*color
            else:
                board[7][3]=0
                board[7][7]=0
                board[7][5]=1000*color
                board[7][4]=5*color

        else:

            if direction == 'king':

                board[0][3]=0
                board[0][0]=0
                board[0][1]=1000*color
                board[0][2]=5*color


            else:
                board[0][3]=0
                board[0][7]=0
                board[0][5]=1000*color
                board[0][4]=5*color

        return board


    def promotePiece(self, color, destination, piece, col=None):
        self.enpassants={-1:[], 1:[]}
        #return a board state with the promotion enacted

        piece=piece[0]
        board = copy.deepcopy(self.board[:])
        if col == None:

            board[destination[0]][destination[1]] = color*piece
            board[destination[0]-color][destination[1]]=0
            return board

        else:
            board[destination[0]][destination[1]] = color*piece
            board[destination[0]-color][col] = 0
            return board

    def enPassantCapture(self, color, origin, destination):
        board=copy.deepcopy(self.board[:])
        self.enpassants={-1:[], 1:[]}
        #return a board state where the enpassant capture has been enacted
        board = self.board[:]
        x1 = origin[0]
        y1 = origin[1]
        x2 = destination[0]
        y2 = destination[1]
        board[x1][y1]=0
        board[x2][y2]=color
        board[x1][y2]=0

        return board

    def simpleMove(self,color,piece, origin, destination):
        self.enpassants={-1:[], 1:[]}
        #return a new board state with the simple move enacted
        board = copy.deepcopy(self.board[:])
        x1 = origin[0]
        y1 = origin[1]
        x2 = destination[0]
        y2 = destination[1]
        board[x1][y1]=0
        board[x2][y2]=piece*color

        if abs(piece) in [1000,-1000]:

            self.canCastle[color*piece]['king']=False
            self.canCastle[color*piece]['queen']=False
        elif abs(piece) in [5,-5]:

            if origin == [0,0]:
                self.canCastle[1000]['king']=False
            elif origin == [7,0]:
                self.canCastle[-1000]['king']=False

            elif origin == [0,7]:
                self.canCastle[1000]['queen']=False

            elif origin == [7,7]:
                self.canCastle[-1000]['queen']=False



        return board

    def moveToInstruction(self,color,move):

        #method for turning the move Instructions from 'miner2.py' into new board states
        #self.enpassants ={-1:[],1:[]}
        cols = move['cols']
        typ=move['type']

        rows=move['rows']


        #searchPiece(self, color, piece, destination, col=None, row=None):
        if typ=='':

            if len(move['piece'])>0:
                piece=move['piece'][0]
                #e.g Nfxe4
                if len(cols)>1 and len(rows)==1:
                    destination = [rows[0],cols[1]]
                    origin = self.searchPieceMove(color,piece,destination,col=cols[0])
                    board=self.simpleMove(color,piece,origin,destination)

                elif len(rows)>1 and len(cols)==1:
                    #e.g N1xe4

                    destination = [rows[1],cols[0]]
                    origin =self.searchPieceMove(color,piece,destination,row=rows[0])
                    board=self.simpleMove(color,piece,origin,destination)

                elif len(rows)>1 and len(cols)>1:
                    #e.g Ne1xe6  #this kind of move wasn't listed in the notation until the 8000th game
                    destination = [rows[1],cols[1]]
                    origin = [rows[0],cols[0]]
                    board = self.simpleMove(color,piece,origin,destination)

                else:
                    #e.g Ne4
                    destination = [rows[0],cols[0]]
                    origin =self.searchPieceMove(color,piece,destination)
                    board=self.simpleMove(color,piece,origin,destination)







            else:
                if len(cols)==1:

                    result = self.searchPawnMove(color, cols[0],'forward',number=rows[0])
                    #e.g e4
                    self.enpassants={-1:[], 1:[]}

                    origin = result['pos']
                    d = [rows[0],cols[0]]
                    board=self.simpleMove(color, 1, origin, d)
                    if abs(rows[0]-result['pos'][0])>1:

                        self.enpassants[color]+=[rows[0],cols[0]]


                else:

                    d=[rows[0],cols[1]]
                    result=self.searchPawnMove(color, cols[0], 'capture', destination=d)
                    origin = result['pos']
                    #e.g exd4
                    if result['type']=='normalCapture':

                        board=self.simpleMove(color, 1, origin, d)


                    #e.g,.....
                    elif result['type']=='epCapture':

                        board=self.enPassantCapture(color,origin,d)





        elif typ == 'promote':
            #e.g cxd8=Q
            if len(cols)>1:
                    board = self.promotePiece(color, [rows[0],cols[1]], move['piece'],col=cols[0])

            else:
                board = self.promotePiece(color, [rows[0],cols[0]], move['piece'])

        elif typ == 'castle':
            #e.g e8=Q
            board = self.castle(color, len(move['castles']))
            self.hasCastled[color*1000]=True

        #check to see if this move is going to disallow castling->
        if self.hasCastled[color*1000] == False and (self.canCastle[color*1000]['king'] == True or self.canCastle[color*1000]['queen']==True):

            if isinstance(move['piece'],int) :

                if abs(move['piece']) ==  1000:

                    self.canCastle[move['piece']]['king']=False
                    self.canCastle[move['piece']]['queen']=False


                elif abs(move['piece'])==5:

                    if color == 1:
                        if origin == [0,0]:
                            self.canCastle[move['piece']]['king']=False
                        elif origin == [0,7]:
                            self.canCastle[move['piece']]['queen']=False
                    else:
                        if origin == [7,0]:
                            self.canCastle[move['piece']]['king']=False
                        elif origin == [7,7]:
                            self.canCastle[move['piece']]['queen']=False




        return board
