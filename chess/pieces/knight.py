from chess.pieces.vc import validCoords


class knight():

    def __init__(self, pieces):

        self.value = pieces['KNIGHT']
        self.pinned = 0



    def canMove(self, origin, destination):

        pass

    def returnValidMoves(self, x, y,color,board,pin):
        self.color=color
        arr = []
        Capturearr=[]
        Protectarr=[]
        result = {'moves':[], 'captures':[], 'protects':[]}

        if pin == None:



            for i in [[2, -1], [2, 1], [-2, 1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]:

                lx=x+i[0]; ly=y+i[1]

                if validCoords(lx,ly):
                    if board[lx][ly] * self.color < 0:

                        result['captures'].append([lx,ly])

                    elif board[lx][ly] * self.color > 0:

                        result['protects'].append([lx,ly])

                    else:
                        result['moves'].append([lx,ly])



        else:
            pass

        return result
