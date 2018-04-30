#the purpose here is not to build an actual predictive model.
import numpy as np
from sklearn.externals import joblib
#rather it's to have A model, like any model, driving things -->
class forest():

    def __init__(self, data=None,pikl=None):

        #the columns to extract for our forest model - just the board and the move number. THe point of this model is that we won't have to calculate game state statistics in order to get a baseline prediction from it.
        if pikl == None and data != None:
        #e.g we can set a threshold at 20-30% or something, and use this model to indentify moves which are not worthy of exploring :)
            cols = ['move','00', '01', '02', '03', '04', '05', '06', '07', '10', '11', '12', '13', '14', '15', '16', '17', '20', '21', '22', '23', '24', '25', '26', '27', '30', '31', '32', '33', '34', '35', '36', '37', '40', '41', '42', '43', '44', '45', '46', '47', '50', '51', '52', '53', '54', '55', '56', '57', '60', '61', '62', '63', '64', '65', '66', '67', '70', '71', '72', '73', '74', '75', '76', '77']

            from sklearn.ensemble import RandomForestClassifier
            import pandas as pd


            self.df = pd.read_csv(data,  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
            self.clf = RandomForestClassifier(max_depth=50,random_state=1)
            self.clf.fit(self.df[cols],self.df['winner'])

        elif pikl != None and data == None:
             self.clf = joblib.load(pikl)

        else:
            ('No data to load and no binaries to pickle. Forest is null...')
            return None
    def evaluate(self, board, moveNumber,color=None):

        array=np.zeros([65],dtype=np.int)
        array[0]=moveNumber
        counter=1
        board = board[:]
        for row in board:

            for cell in row:
                array[counter]=cell
                counter+=1
        print('preditced winnder:', self.clf.predict([array])[0])
        prediction = self.clf.predict_proba([array])
        print(prediction)
        if color != None:
            return prediction[0][0]

        return prediction

    def makePiklDump(self,piklName):

        joblib.dump(self.clf, piklName)

if __name__ == '__main__':

    f=forest(pikl='data/forestmodelDepth20.pkl')
