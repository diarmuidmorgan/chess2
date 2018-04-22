import pawn
import king
import rook
import knight
import bishop
import queen

pieces = {'PAWN':8, 'ROOK': 2, 'KNIGHT':2, 'BISHOP':2, 'KING':1, 'QUEEN':1}
values = {'PAWN':1, 'KNIGHT':3, 'BISHOP':4, 'ROOK':5, 'QUEEN':9, 'KING':1000}


p = pawn.pawn(pieces)
k=king.king(pieces)
r=rook.rook(pieces)
N=knight.knight(pieces)
b=bishop.bishop(pieces)
q=queen.queen(pieces)

board = [[5,3,4,1000,9,4,3,5],
[1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[-1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[-1,-1,-1,-1,-1,-1,-1,-1],
[-5,-3,-4,-1000,-9,-4,-3,-5],]

#pins are working now, kind of.
print(p.returnValidMoves(4,1,1,board,{1:[],-1:[[4,0]]},None))
print(q.returnValidMoves(4,4,1,board,None))
print(r.returnValidMoves(5,5,1,board,[[1,1],[-1,-1]]))
print(k.returnValidMoves(5,5,1,board,[[4,5], [5,4]]))
print(N.returnValidMoves(5,5,1,board,[1,1]))
print(b.returnValidMoves(5,5,1,board,[[1,1],[-1,-1]]))
