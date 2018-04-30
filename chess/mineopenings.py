import pandas as pd
df=pd.read_csv('data/finalExplodedChess.csv')
ids = df['id'].unique()
def makeBoard(row):
    board=[]
    for x in range (0, 8):
        board.append([])
        for y in range(0, 8):
            board[x].append(int(row[str(x)+str(y)]))

    return(board)

def score(row):

    if row['winner']=='white':
        return 1
    else:
        return 0

j={'games':[]}

import json

for game_id in range(0, 5000):

    simp_df=df[df['id']==ids[game_id]]
    currentArr = j['games']
    if simp_df['move'].max()<10:
        r=simp_df['move'].max()+1
    else:
        r=10

    for move in range(1, r):

        new_board = makeBoard(simp_df[simp_df['move']==move].iloc[0])
        quickscore = score(simp_df[simp_df['move']==move].iloc[0])
        obj=[new_board, [], quickscore, 0]
        found=False
        if len(currentArr)!=0:
            for index, thing in enumerate(currentArr):

                if thing[0] == obj[0]:
                    found=True
                    q=index
                    break
        if found == True:
            currentArr[q][2]=((currentArr[q][2]*currentArr[q][3])+quickscore)/(currentArr[q][3]+1)
            currentArr[q][3]+=1

            currentArr = currentArr[q][1]

        else:
            currentArr.append(obj)
            currentArr = currentArr[-1][1]


f = open('data/openings.json','w')
f.write(json.dumps(j))
f.close()
