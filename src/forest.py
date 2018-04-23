from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.externals import joblib
import pandas as pd
import stats
import json

class forest():

    def __init__(self, from_pikl=False):

        self.an = stats.analyze()
        if not from_pikl:

            self.buildModel()


        else:

            self.model=joblib.load('data/forest.pikl')
            self.features = json.load(open('data/features'))['features']

    def buildModel(self):

        nums=[str(i) for i in range (8)]
        df = pd.read_csv('data/finalExplodedChess.csv')
        numbers = [str(i) for i in range(8)]
        cols = [col for col in df.columns if col not in ['white_rating', 'opening', 'black_rating', 'id', 'victory_type']]
        print(cols)
        cols = [col for col in cols if col[0] not in numbers]

        features_to_concat=[df]
        features_to_concat.append(pd.get_dummies(df['winner'], prefix='winner'))
        df = pd.concat(features_to_concat, axis=1)
        cols = [col for col in cols if col not in ['winner',  'target', 'winner_white', 'winner_black']]
        df = pd.concat(features_to_concat, axis=1)
        print(df[cols].shape)
        clf = rf(max_depth=100).fit(df[cols], df['winner_white'])
        joblib.dump(clf, 'data/forest.pikl')
        import json
        f=open('data/features','w')
        f.write(json.dumps({'features':cols}))
        f.close()
        print(cols)

    def score(self,gstate, moveNum, color):

        X=self.an.analyze(moveNum, gstate, True)
        #see if this is the fucking issue!


        bscore = self.model.predict_proba(X[self.features])
        
        return bscore[0][1]






if __name__ == '__main__':

    f=forest(from_pikl=False)
