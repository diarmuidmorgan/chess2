
class rootNode():
    #most simple prototype. Use random forest to score the board, not the gamestate. Only searches the top nodes in the tree.


    def __init__(self, gs, movenumber, forestmodel):
        import copy
        from math import inf
        #takes a preprocessed game state
        self.gamestate = gs
        self.forestmodel = forestmodel
        self.movenumber=movenumber
        print(self.gamestate.castles)


    def search(self,color):
        import copy
        board = copy.deepcopy(self.gamestate.board[:])
        from math import inf

        self.alpha = inf
        self.beta = inf



        self.bestMove = []

        if self.gamestate.castles[color*1000]['king']==True:
            pboard = gamestate.castle(color, 2)
            base_score = self.forestnodel.evaluate(pboard, self.movenumber,color)
            if base_score < self.alpha:
                self.alpha = base_score
                self.bestMove = {'castle':'king'}
        elif self.gamestate.castles[color*1000]['queen']==True:
            pboard = gamestate.castle(color, 3)
            base_score = self.forestmodel.evaluate(board, self.movenumber,color)
            if base_score < self.alpha:
                self.alpha = base_score
                self.bestMove = {'castle':'king'}




        for move in self.gamestate.captures[color]:
            print(move)

            pboard = copy.deepcopy(board[:])

            origin=move['origin']
            destination = move['destination']
            pboard[destination[0]][destination[1]]=pboard[origin[0]][origin[1]]
            pboard[origin[0]][origin[1]]=0
            base_score = self.forestmodel.evaluate(pboard, self.movenumber, color)
            if base_score < self.alpha:
                self.alpha = base_score
                self.bestMove = move




        for move in self.gamestate.moves[color]:
            print(move)
            pboard=copy.deepcopy(board[:])

            origin=move['origin']
            destination = move['destination']
            pboard[destination[0]][destination[1]]=board[origin[0]][origin[1]]
            pboard[origin[0]][origin[1]]=0
            base_score = self.forestmodel.evaluate(pboard, self.movenumber, color)
            if base_score < self.alpha:
                self.alpha = base_score
                self.bestMove = move

        for move in self.gamestate.enpassants[color]:

            pboard=self.gamestate.EnpassantCapture(origin, color, destination)
            base_score = self.forestmodel.evaluate(pboard, self.movenumber,color)
            if base_score < self.alpha:
                self.alpha = base_score
                self.bestMove = move

        print(self.bestMove)
        return self.bestMove
