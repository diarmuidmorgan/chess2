from chess import gs
from chess import stats
from chess import pieces
from chess import models
from chess import forest
import copy
from operator import itemgetter
import random
class thinker():


    def __init__(self):
        self.forest = forest.forest(from_pikl=True)
        pass


    def rootthink(self,gs, color, moveNum, searchdepth=1):

        gs = copy.deepcopy(gs)

        gs.getPinnedSquares()
        gs.pinPieces()
        gs.getAllMoves()


        best_score = 1
        best_move = []
        best_gs=copy.deepcopy(gs)

        for castle in gs.castles[color*1000]:
            new_gs = copy.deepcopy(gs)


            if gs.castles[color*1000][castle] == True and random.random()>0:

                if castle=='king':
                    number=2
                else:
                    number=3

                new_board = gs.castle(color, number)
                score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
                print('win prob:', 1-score)
                if score < best_score:
                    best_score = score
                    best_move ={'type':'castle', 'number':number}
                    best_gs = copy.deepcopy(new_gs)

        for capture in gs.captures[color]:
            if random.random()>0:
                new_gs = copy.deepcopy(new_gs)
                origin = capture['origin']
                destination = capture['destination']
                piece = abs(gs.board[origin[0]][origin[1]])
                new_board = new_gs.simpleMove(color, piece, origin, destination)
                score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
                print('win prob:', 1-score)
                if score < best_score:
                    best_score = score
                    best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                    best_gs=copy.deepcopy(new_gs)



        for move in gs.moves[color]:
            if random.random()>0:
                new_gs = copy.deepcopy(gs)
                origin = move['origin']
                destination = move['destination']

                piece = abs(new_gs.board[origin[0]][origin[1]])
                new_board = new_gs.simpleMove(color, piece, origin, destination)

                score = self.node_search(new_gs.returnNewGameState(new_board), moveNum, color,depth=searchdepth)
                print('win prob:', 1-score)
                if score < best_score:
                    best_score = score
                    best_move = {'type':'simple', 'origin':origin, 'destination':destination}
                    best_gs = copy.deepcopy(new_gs)
        print('Best move:', best_move, 'win prob:', 1-best_score)
        return best_move


    def node_search(self,gs, moveNum, color, depth=0, base_score=None):
        moveNum+=1
        results=[]
        if base_score==None:
            gs=copy.deepcopy(gs)
            gs.getPinnedSquares()
            gs.pinPieces()
            gs.getAllMoves()
            base_score = self.forest.score(gs, moveNum, color)

        if gs.checked == color:
            print('checked')
            if color == -1:
                return 1
            else:
                return 0

        if (color == 1 and base_score < 0.3) or (color == -1 and base_score > 0.7):
            return base_score

        best_score=0.5
        if depth == 0:
            return base_score

        d=depth-1
        color=color*-1

        for castle in gs.castles[color*1000]:
            new_gs = copy.deepcopy(gs)


            if new_gs.castles[color*1000][castle] == True and random.random()>0:

                if castle=='king':
                    number=2
                else:
                    number=3
                m={'type':'castle', number:'number'}
                new_board = new_gs.castle(color, number)
                g=new_gs.returnNewGameState(new_board)
                results.append(self.quickScore(g, moveNum, color, m))


        for capture in gs.captures[color]:
            if random.random()>0:
                new_gs = copy.deepcopy(new_gs)
                origin = capture['origin']
                destination = capture['destination']
                m = {'type':'simple', 'origin':origin, 'destination':destination}
                piece = abs(new_gs.board[origin[0]][origin[1]])
                new_board = new_gs.simpleMove(color, piece, origin, destination)
                g=new_gs.returnNewGameState(new_board)
                results.append(self.quickScore(g, moveNum, color, m))





        for move in gs.moves[color]:
            if random.random()>0:
                new_gs = copy.deepcopy(gs)
                origin = move['origin']
                destination = move['destination']
                m = {'type':'simple', 'origin':origin, 'destination':destination}

                piece = abs(new_gs.board[origin[0]][origin[1]])
                new_board = new_gs.simpleMove(color, piece, origin, destination)

                g=new_gs.returnNewGameState(new_board)
                results.append(self.quickScore(g, moveNum, color, m))




        results = sorted(results, key=itemgetter('score'))


        if color == -1:
            begin = 0
            end = min(5, len(results))
            increment = 1
            best_score=1
            for i in range(begin, end, increment):

                result=results[i]
                new_score = self.node_search(result['gs'], moveNum, color, depth=d, base_score=result['score'])
                if new_score < best_score:
                    best_score = new_score

        else:
            begin = len(results)-1
            end = max(len(results)-6,0)
            increment = -1
            best_score=0

            for i in range(begin, end, increment):

                result=results[i]
                new_score = self.node_search(result['gs'], moveNum, color, depth=d, base_score=result['score'])
                if new_score > best_score:
                    best_score = new_score


        return best_score



    def quickScore(self,gs, moveNum, color, move):

        gs=copy.deepcopy(gs)
        gs.getPinnedSquares()
        gs.pinPieces()
        gs.getAllMoves()
        if gs.checked == color:
            if color == -1:
                base_score= 10
            else:
                base_score = -10


        else:
            base_score = self.forest.score(gs, moveNum, color)

        return {'score':base_score, 'gs':gs, 'move':move}







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
