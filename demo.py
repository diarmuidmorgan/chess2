#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:56:22 2018

@author: eoin
"""

import chess.miner as miner
import pandas as pd
games = pd.read_csv('chess/data/cleanChess.csv')
games_exploded = miner.mine(games.iloc[0])

def exploder(x):
    limit = min(500 * x, games.shape[0])
    start = limit - 500
    games_exploded = miner.mine(games.iloc[start])
    for i in range(start+1, limit):
        if ((i-1) % 100 == 0):
            print("Games Exploded:", i, '/', games.shape[0])
        try:
            exploded_game = miner.mine(games.iloc[i])
            games_exploded = games_exploded.append(exploded_game)
        except Exception as e:
            print("Error on game:", i, "Reason:", e)
    games_exploded.to_csv('data/explodedCleanChess' + str(x) + '.csv', index=False)

def exploder2():
    games_exploded = miner.mine(games.iloc[0])
    limit = games.shape[0]
    count = 1
    for i in range(1, limit):
            exploded_game = miner.mine(games.iloc[i])
            games_exploded = games_exploded.append(exploded_game)
            if i % 100 == 0:
                print("Games Exploded:", i, '/', limit)
                if i % 500 == 0:
                    games_exploded.to_csv('chess/data/explodedCleanChess' + str(count) + '.csv', index=False)
                    count += 1
                    games_exploded = games_exploded[games_exploded.id == "test"]
    if games_exploded.shape[0] > 0:
        games_exploded.to_csv('chess/data/explodedCleanChess' + str(count) + '.csv', index=False)



if __name__ == '__main__':
    exploder2()
