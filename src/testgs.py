import gs as gs

board = [[5,3,4,1000,9,4,3,5],
[1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0],
[-4,0,0,-9,0,0,0,0],
[-1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[-1,-1,-1,-1,-1,-1,-1,-1],
[-5,-3,-4,-1000,-9,-4,-3,-5],]
g=gs.gamestate(board, {-1:[], 1:[]},[],[])
g.getPinnedSquares()
g.pinPieces()
g.getAllMoves()
g.representBoard()
print(g.scoreMaterial())
print(g.collection)
t=g.returnNewGameState()
