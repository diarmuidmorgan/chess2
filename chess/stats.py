import numpy as np
import pandas as pd
def validCoords(x,y):

    if x>=0 and x<8 and y>=0 and y<8:

        return True
    else:
        return False


class analyze():


    def __init__(self, state=None):

        if state != None:

            self.loadState(state)


        pass



    def loadState(self,state,move=None):
        if move!=None:
            self.move = move
        self.moves=0
        self.captures=0
        self.protected=0
        self.forks = 0
        self.basicScore = 0
        self.pawnLines = 0
        self.stackedPawns = 0
        self.centrePawns = 0
        self.pawnsGuardingKings = 0
        self.kingMoves = 0
        self.pawnRanks = 0
        self.fianchettos = 0
        self.state = state
        self.collection = state.collection
        self.board = state.board
        self.checked = state.checked
        self.protectingPieces=0
        #will do these another night
        self.hasCastled = state.hasCastled[1000]-state.hasCastled[-1000]
        self.canCastle = int(state.canCastle[1000]['king'])+int(state.canCastle[1000]['queen'])-int(state.canCastle[-1000]['king'])-int(state.canCastle[-1000]['queen'])
        self.enpassants = len(state.enpassants[1])-len(state.enpassants[-1])

        self.pins=len(state.pinnedSquares[1000]) - len(state.pinnedSquares[-1000])
    def readCollection(self):

        for pieceType in self.collection:


            for piece in self.collection[pieceType]:

                color = int(pieceType/abs(pieceType))

                self.moves += len(piece['moves']) * color

                if abs(pieceType) == 1000:

                    self.kingMoves += len(piece['moves']) * color

                for pos in piece['captures']:

                    x=pos[0];y=pos[1]
                    self.captures += self.board[x][y]

                    if len(piece['captures'])>1:

                        self.forks+=self.board[x][y]

                for pos in piece['protects']:

                    x=pos[0];y=pos[1]
                    self.protected += self.board[x][y]
                    self.protectingPieces += pieceType

                if piece['pin']!=None:

                    self.pins+=color

    def scoreBoard(self):
        board=self.board
        # should return a sum of all the pieces on the scoreBoard
        #should be zero, if both black and white have the same material
        #while examining the board, it also tries to count lines of pawns, stacks of pawns, and the amount of pawns currently guaring the king, all of which I feel could be valuable statistics
        for x,row in enumerate(self.board):

            for y,cell in enumerate(row):

                #get basic material score as a negative or positive integer
                if cell == -4:

                    #if they're fucking bishops, got to take 1 off the score
                    self.basicScore += -3
                elif cell == 4:
                    self.basicScore += 3

                else:

                    self.basicScore += cell

                #also check and score amount of pawns guarding king
                if int(abs(cell))==1000:

                    color = int(cell/abs(cell))
                    direction = color

                    for coords in [[x+direction, y-1],[x+direction,y],[x+direction,y]]:

                        if validCoords(coords[0], coords[1]):

                            if board[coords[0]][coords[1]]==color:

                                self.pawnsGuardingKings += color



                #also score pawn ranks
                elif abs(cell)==1:

                    color = int(cell/abs(cell))
                    direction = color * -1
                    if color == 1:

                        self.pawnRanks+= x

                    else:
                        self.pawnRanks -= 7-x

                    #also count lines of pawns
                    for lr in [-1,1]:

                        if validCoords(x+direction, y+lr):

                            if board[x+direction][y+lr]==color:

                                self.pawnLines += color

                    #also count stacked pawns

                    if validCoords(x-direction,y):

                        if board[x-direction][y] == color:

                            self.stackedPawns += color

    def findFianchetto(self):
        #sum the fianchetto squares on the board
        if self.board[1][1]==4:

            self.fianchettos +=1

        if self.board[1][6]==4:
            self.fianchettos +=1

        if self.board[6][6]==-4:
            self.fianchettos -=1

        if self.board[6][1]==-4:

            self.fianchettos -=1

    def sumCentrePawns(self):
        #return a sum of the pawns in the four centre squares
        board=self.board
        for coords in [[3,4],[3,3],[4,4], [4,3]]:

            if abs(board[coords[0]][coords[1]])==1:

                self.centrePawns += board[coords[0]][coords[1]]
    def sumBackRanks(self):

        self.backRanks = sum(self.board[0])+sum(self.board[7])

        return sum

    def analyze(self, move=None, gs=None, RETURN=False):

        if gs != None and move!=None:
            self.loadState(gs, move)
        if move!=None:
            self.move = move

        self.sumCentrePawns()
        self.findFianchetto()
        self.scoreBoard()
        self.sumBackRanks()
        self.readCollection()
        self.sumBackRanks()
        if RETURN:
            return self.produceX()


    def produceX(self):
        d={}

        d['pawnsGuardingKings']=self.pawnsGuardingKings
        d['possible_moves']=self.moves
        d['captures']=self.captures
        d['forks']=self.forks
        d['basicScore']=self.basicScore
        d['protects']=len(self.state.protects[1])-len(self.state.protects[-1])
        d['pins']=self.pins
        d['centrePawns']=self.centrePawns
        d['kingMoves']=self.kingMoves
        d['pawnRanks']=self.pawnRanks
        d['fianchettos']=self.fianchettos
        d['stackedPawns']=self.stackedPawns
        d['enpassants']=self.enpassants
        d['canCastle']=self.canCastle
        d['pawnLines']=self.pawnLines
        d['hasCastled']=self.hasCastled
        d['checked']=self.checked
        d['protectingPieces']=self.protectingPieces
        d['backRanks']=self.backRanks
        for x in range(8):

            for y in range(8):

                d[str(x)+str(y)]=self.board[x][y]

        d['turns_taken_so_far']=self.move

        row=pd.DataFrame([d], columns=d.keys())
        return row


    def produceStateArray(self):

        self.arr =np.zeros(83, dtype=np.int)
        count=0
        for x in range(0, len(self.board)):

            for y in range(0, len(self.board[x])):


                self.arr[count]=self.board[x][y]
                count+=1

        #so 63 columns of the array have being filled, though it's likely we'll drop these in the future

        self.arr[64]=self.moves
        self.arr[65]=self.captures
        self.arr[66]=self.protected
        self.arr[67]=self.forks
        self.arr[68]=self.basicScore
        self.arr[69]=self.pins
        self.arr[70]=self.centrePawns
        self.arr[71]=self.pawnsGuardingKings
        self.arr[72]=self.kingMoves
        self.arr[73]=self.pawnRanks
        self.arr[74]=self.fianchettos
        self.arr[75]=self.checked
        self.arr[76]=self.pawnLines #currently not done
        self.arr[77]=self.stackedPawns
        self.arr[78]=self.enpassants
        self.arr[79]=self.canCastle
        self.arr[80]=self.hasCastled
        self.arr[81]=self.protectingPieces
        self.arr[82]=self.backRanks


        return self.arr

        #there you go. 64 board squares and fifteen derived features
