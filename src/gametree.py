class game_node():

    def __init__(self, depth, board, enpassants, hasCastled, canCastle):

        self.depth=depth
        self.board = board
        self.enpassants = enpassants
        self.hasCastled = hasCastled
        self.canCastle = canCastle
        self.children = []

    def addChild(self, board, enpassants, hasCastled, canCastle):

        self.children.append(game_node(self.depth+1, board, enpassants, hasCastled, canCastle))

    def hasChild(self, board, enpassants, hasCastled, canCastle):

        for gn in self.children:

            if gn.board == board and gn.enpassants == enpassanats and gn.hasCastled == hasCastled and gn.canCastle == canCastle:

                return True

            else:

                return False

    def createState(self):

        return gamestate(self.board, self.enpassants, self.hasCastled, self.canCastle)

    def getNthChild(self,n):

        return self.children[n]

class gameTree():

    def __init__(self, board, enpassants, hasCastled, canCastle):

        self.root = game_node(0,board, enpassants, hasCastled, canCastle)
        self.position = 0

    def makePikl(self,fileName):
        import pickle
        f=open('fileName', 'w')
        pickle.dump(self, f)

    def returnNode(self,indexes):


        current_node=self.root
        for index in indexes:

            current_node=current_node.getNthChild(index)

        return current_node

tree=gameTree([2,3],0,0,0)

import pickle
f=open('fileName', 'w')
string=pickle.dumps(tree)
f.write(string)
f.close()
