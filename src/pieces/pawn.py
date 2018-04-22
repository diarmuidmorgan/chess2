from pieces.vc import validCoords

class pawn():

    def __init__(self, pieces):

        pass



    def canMove(self, origin, destination):

        pass

    def returnValidMoves(self, x, y, color,board, enpassants,pin):
        enpassants = [enpassants]
        self.color = color
        #this is the result object that the pawn returns
        result={'moves':[], 'checked':[], 'captures':[], 'protects':[], 'ep':[]}
        direction=self.color


        if pin == None:

        #consider forward moves
            try:
                if board[x+direction][y]==0:

                    result['moves'].append([x+direction, y])

                    #check that pawns are on the right rank to move two squares

                    if self.color == 1 and x==1 and board[x+2*direction][y]==0:

                        result['moves'].append([x+2*direction, y])

                    elif self.color == -1 and x == 6 and board[x+2*direction][y]==0:

                        result['moves'].append([x+2*direction, y])
            except:
                print(board)
                print(x,y)

    #consider diagonal capture moves

            if y < 7:


                if board[x+direction][y+1]*self.color<0:

                    result['captures'].append([x+direction, y+1])

                elif board[x+direction][y+1]*self.color>0:

                    result['protects'].append([x+direction, y+1])

                else:
                    result['checked'].append([x+direction, y+1])

                #the piece that can be taken
                if [x,y+1] in enpassants:


                    #records the square the pice can move to
                    #as this is what is listed in the PGN notation
                    result['ep'].append([x+direction,y+1])


            if y>0:

                if board[x+direction][y-1]*self.color<0:

                    result['captures'].append([x+direction, y-1])

                elif board[x+direction][y-1]*self.color>0:

                    result['protects'].append([x+direction, y-1])

                else:
                    result['checked'].append([x+direction, y-1])




                if [x,y-1] in enpassants:



                    #records the square the piece can move to
                    result['ep'].append([x+direction,y-1])

        else:


            #if pinned the vertical is free
            if pin[0] in [[1,0], [-1, 0]]:

                if board[x+direction][y]==0:

                    result['moves'].append([x+direction, y])

                    #check that pawns are on the right rank to move two squares

                    if self.color == 1 and x==1 and board[x+2*direction][y]==0:

                        result['moves'].append([x+2*direction, y])

                    elif self.color == -1 and x == 6 and board[x+2*direction][y]==0:

                        result['moves'].append([x+2*direction, y])
                #[[1,1], [-1, -1], [1,-1], [-1,1]]


                #if right diagonal is free
            elif pin[0] in [[1,1], [-1, -1]]:

                if y < 7 and color == 1:


                    if board[x+direction][y+1]*self.color<0:

                        result['captures'].append([x+direction, y+1])

                    elif board[x+direction][y+1]*self.color>0:

                        result['protects'].append([x+direction, y+1])

                    else:
                        result['checked'].append([x+direction, y+1])

                        #enpassants should record the square the pawn can take. The pawn returns the square it can move to..!
                    if [x,y+1] in enpassants:

                        #records the square the piece can move to
                        result['ep'].append([x+direction,y+1])

                if y>0 and color == -1:

                    if board[x+direction][y-1]*self.color<0:

                        result['captures'].append([x+direction, y-1])

                    elif board[x+direction][y-1]*self.color>0:

                        result['protects'].append([x+direction, y-1])

                    else:
                        result['checked'].append([x+direction, y-1])




                    if [x,y-1] in enpassants:

                        #records the square the piece can move to
                        #not the square that it can take
                        result['ep'].append([x+direction,y-1])


            #if left diagonal is free
            elif pin[0] in [[1,-1], [-1,1]]:

                if y>0 and color == 1:

                    if board[x+direction][y-1]*self.color<0:

                        result['captures'].append([x+direction, y-1])

                    elif board[x+direction][y-1]*self.color>0:

                        result['protects'].append([x+direction, y-1])

                    else:
                        result['checked'].append([x+direction, y-1])




                    if [x,y-1] in enpassants:

                        #records the square the piece can move to
                        result['ep'].append([x+direction,y-1])

                if y < 7 and color == -1:


                    if board[x+direction][y+1]*self.color<0:

                        result['captures'].append([x+direction, y+1])

                    elif board[x+direction][y+1]*self.color>0:

                        result['protects'].append([x+direction, y+1])

                    else:
                        result['checked'].append([x+direction, y+1])


                    if [x,y+1] in enpassants:

                        #records the square the piece can move to
                        result['ep'].append([x+direction,y+1])

        return result
