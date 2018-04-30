from chess.pieces.vc import validCoords

class king():
    #haven't added a method to check for moves causing check
    #same as there isn't a method to check for pins

    #need to think of an efficient method for checking these two things

    def __init__(self, pieces):

        self.value = pieces['KING']
        self.pinned = False
        self.checked = False



    def canMove(self, origin, destination):

        pass

    def returnValidMoves(self, x, y, color, board, checkSquares):
        #using checkSquares resolves illegal moves, but not pins.
        arr = []
        Capturearr = []
        Protectarr = []
        self.color = color
        #print('color: ', color, '\n', 'checksquares:',checkSquares)


        for i in [[1,0], [-1, 0], [0,-1], [0,1],[1,1], [-1, -1], [1,-1], [-1,1]]:

            ix = i[0]; iy = i[1]
            lx = x+ix; ly = y+iy
            dummy=[[500,500]]
            if validCoords(lx,ly):

                if  [lx,ly] not in checkSquares:
                    #print(board[lx][ly])
                    if board[lx][ly] == 0:
                        arr.append([lx,ly])
                        #print(True)

                    elif board[lx][ly]*self.color<0:
                        Capturearr.append([lx,ly])

                    else:
                        Protectarr.append([lx,ly])




        return {'moves':arr, 'captures':Capturearr, 'protects':Protectarr}

    def isChecked(self, x, y, checkedSquares):

        if [x,y] in checkedSquares:

            return True

        else:
            return False

    def returnPins(self, x, y, color,board):
        #sloppy method for finding pinned pieces

        pins={}


        #check verticals
        for i in [[1,0], [-1, 0], [0,-1], [0,1]]:

            ix = i[0]; iy = i[1]
            lx = x; ly = y
            Protected = False



            while True:

                lx+=ix; ly+=iy

                if validCoords(lx,ly):
                    if board[lx][ly]*color>=1:

                        if Protected:
                            break

                        else:
                            Protected = True
                            pin=[lx,ly]

                    elif board[lx][ly]*color<0:

                        if abs(board[lx][ly]) in [5,9] and Protected:

                            if i in [[1,0],[-1,0]]:
                                okdirections = [[1,0],[-1,0]]
                            else:
                                okdirections = [[0,-1], [0,1]]

                            pins[str(pin[0])+str(pin[1])]=okdirections
                            break
                        else:
                            break

                else:

                    break

        #check diagonals
        for i in [[1,1], [-1, -1], [1,-1], [-1,1]]:

            ix = i[0]; iy = i[1]
            lx = x; ly = y
            Protected = False


            while True:

                lx+=ix; ly+=iy

                if validCoords(lx, ly):
                    if board[lx][ly]*color>=1:

                        if Protected:
                            break

                        else:
                            Protected = True
                            pin=[lx,ly]

                    elif board[lx][ly]*color<0:

                        if abs(board[lx][ly]) in [4,9] and Protected:

                            if i in [[1,1], [-1, -1]]:
                                okdirections = [[1,1], [-1, -1]]
                            else:
                                okdirections = [[1,-1], [-1,1]]

                            pins[str(pin[0])+str(pin[1])]=okdirections
                            break

                        else:
                            break

                else:


                    break

        return pins
