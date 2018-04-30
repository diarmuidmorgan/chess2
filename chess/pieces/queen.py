from chess.pieces.vc import validCoords

class queen():
    #just a bishop and a rook
    def __init__(self, pieces):

        self.value = pieces['QUEEN']
        self.pinned = 0



    def canMove(self, origin, destination):

        pass

    def returnValidMoves(self, x, y, color,board,pin):
        self.color = color
        arr = []
        Capturearr = []
        Protectarr=[]

        if pin == None:

            for i in [[1,0], [-1, 0], [0,-1], [0,1],[1,1], [-1, -1], [1,-1], [-1,1]]:

                ix = i[0]; iy = i[1]
                lx = x; ly = y
                blocked = False

                while not blocked:

                    lx+=ix; ly+=iy

                    if validCoords(lx,ly):

                        if board[lx][ly] == 0:

                            arr.append([lx,ly])

                        elif board[lx][ly] * self.color < 0:


                            Capturearr.append([lx, ly])
                            blocked = True
                            break

                        else:
                            blocked = True
                            Protectarr.append([lx,ly])
                            break

                    else:
                        blocked = True
                        break

        else:
            
            for i in [[1,0], [-1, 0], [0,-1], [0,1],[1,1], [-1, -1], [1,-1], [-1,1]]:
                if i in pin:

                    ix = i[0]; iy = i[1]
                    lx = x; ly = y
                    blocked = False

                    while not blocked:

                        lx+=ix; ly+=iy

                        if validCoords(lx,ly):

                            if board[lx][ly] == 0:

                                arr.append([lx,ly])

                            elif board[lx][ly] * self.color < 0:


                                Capturearr.append([lx, ly])
                                blocked = True
                                break

                            else:
                                blocked = True
                                Protectarr.append([lx,ly])
                                break

                        else:
                            blocked = True
                            break

        return {'moves':arr, 'captures':Capturearr, 'protects':Protectarr}
