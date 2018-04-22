import gs
import stats
import pieces
import models
import forest
import copy

class thinker():


    def __init__(self):
        self.forest = forest.forest(from_pikl=True)
        pass


    def rootthink(self,gs, color, moveNum):
        searchdepth=1
        gs = copy.deepcopy(gs)

        gs.getPinnedSquares()
        gs.pinPieces()
        gs.getAllMoves()


        best_score = -1
        best_move = []
        best_gs=copy.deepcopy(gs)

        for castle in gs.castles[color*1000]:
            new_gs = copy.deepcopy(gs)


            if gs.castles[color*1000][castle] == True:

                if castle=='king':
                    number=2
                else:
                    number=3

                new_board = gs.castle(color, number)
                score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
                if score > best_score:
                    best_score = score
                    best_move ={'type':'castle', 'number':number}
                    best_gs = copy.deepcopy(new_gs)

        for capture in gs.captures[color]:
            new_gs = copy.deepcopy(new_gs)
            origin = capture['origin']
            destination = capture['destination']
            piece = abs(gs.board[origin[0]][origin[1]])
            new_board = new_gs.simpleMove(color, piece, origin, destination)
            score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
            if score > best_score:
                best_score = score
                best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                best_gs=copy.deepcopy(new_gs)



        for move in gs.moves[color]:
            new_gs = copy.deepcopy(gs)
            origin = move['origin']
            destination = move['destination']

            piece = abs(new_gs.board[origin[0]][origin[1]])
            new_board = new_gs.simpleMove(color, piece, origin, destination)

            score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
            if score > best_score:
                best_score = score
                best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                best_gs = copy.deepcopy(new_gs)
        print(best_score)
        return best_move


    def node_search(self,gs, moveNum, color, depth=0, base_score=False):
        if base_score == False:
            gs=copy.deepcopy(gs)
            gs.getPinnedSquares()
            gs.pinPieces()
            gs.getAllMoves()
            base_score = self.forest.score(gs, moveNum, color)
        if gs.checked == color:
            return 0


        best_score=0
        if depth == 0:
            return base_score

        d=depth-1
        color=color*-1

        for castle in gs.castles[color*1000]:
            new_gs = copy.deepcopy(gs)


            if new_gs.castles[color*1000][castle] == True:

                if castle=='king':
                    number=2
                else:
                    number=3

                new_board = new_gs.castle(color, number)
                score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=d)
                if score > best_score:
                    best_score = score
                    best_move ={'type':'castle', number:'number'}
                    best_gs = copy.deepcopy(new_gs)

        for capture in gs.captures[color]:
            new_gs = copy.deepcopy(new_gs)
            origin = capture['origin']
            destination = capture['destination']
            piece = abs(new_gs.board[origin[0]][origin[1]])
            new_board = new_gs.simpleMove(color, piece, origin, destination)
            score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=d)
            if score > best_score:
                best_score = score
                best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                best_gs=copy.deepcopy(new_gs)



        for move in gs.moves[color]:
            new_gs = copy.deepcopy(gs)
            origin = move['origin']
            destination = move['destination']

            piece = abs(new_gs.board[origin[0]][origin[1]])
            new_board = new_gs.simpleMove(color, piece, origin, destination)

            score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=d, base_score = move['score'])
            if score > best_score:
                best_score = score
                best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                best_gs = copy.deepcopy(new_gs)

        return max(base_score - best_score,0)




    def quickScore(gs, moveNum, color):

        gs=copy.deepcopy(gs)
        gs.getPinnedSquares()
        gs.pinPieces()
        gs.getAllMoves()
        if gs.checked == color:
            base_score=0

        else:
            base_score = self.forest.score(gs, moveNum, color)

        return {'score':base_score, 'gs':gs}





        return best_gamestate

if __name__=='__main__':
    think = thinker()
    board = [[5,3,4,1000,9,4,3,5],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,-1,-1,-1,-1,-1,-1,-1],
    [-5,-3,-4,-1000,-9,-4,-3,-5],]
    ep={-1:[], 1:[]}

    canCastle = {1000:{'queen':True, 'king':True}, -1000:{'queen':True, 'king':True}}
    hasCastled = {1000:False, -1000:False}

    color=-1
    ep={-1:[], 1:[]}

    state = gs.gamestate(board, ep, canCastle, hasCastled)

    print(think.rootthink(state,1, 1))
