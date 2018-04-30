from chess.pieces.vc import validCoords

class bishop():

    def __init__(self, pieces):

        self.value = pieces['BISHOP']
        self.pinned = 0


    def canMove(self, origin, destination):

        pass

    def returnValidMoves(self, x, y, color,board,pin):
        self.color = color
        arr = []
        Capturearr=[]
        Protectarr = []
        result={'moves':[], 'captures':[], 'protects':[]}
        if pin == None:



            for i in [[1,1], [-1, -1], [1,-1], [-1,1]]:

                ix = i[0]; iy = i[1]
                lx = x; ly = y
                blocked = False

                while not blocked:

                    lx+=ix; ly+=iy

                    if validCoords(lx,ly):

                        if board[lx][ly] == 0:

                            result['moves'].append([lx,ly])

                        elif board[lx][ly] * self.color < 0:

                            blocked = True
                            result['captures'].append([lx, ly])

                        else:

                            blocked = True
                            result['protects'].append([lx, ly])

                    else:
                        blocked = True

        else:

            for i in [[1,1], [-1, -1], [1,-1], [-1,1]]:

                if i in pin:
                    ix = i[0]; iy = i[1]
                    lx = x; ly = y
                    blocked = False

                    while not blocked:

                        lx+=ix; ly+=iy

                        if validCoords(lx,ly):

                            if board[lx][ly] == 0:

                                result['moves'].append([lx,ly])

                            elif board[lx][ly] * self.color < 0:

                                blocked = True
                                result['captures'].append([lx, ly])

                            else:

                                blocked = True
                                result['protects'].append([lx, ly])

                        else:
                            blocked = True


        return result
