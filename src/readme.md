** Chess **  

Collection of modules for analyzing and playing chess games.

** gamestring.py ** contains methods for reading moves from PGN notation, and playing a game of such moves, outputting it as an array.

** Gametree.py ** is an unfinished module, containing an unfinished class for representing a gametree

The ** pieces * folder contains a module/class for each piece, with methods for finding valid moves, and in the case of the king, determining check and locating pinned pieces,

** gs.py contains ** the gamestate class. This is by far the most complicated part, and I feel as if too many different methods have been packed into it.

It maps pieces into a collection, and contains methods for managing and moving the pieces on the board, as well as returning new board states.

** stats.py ** contains the class analyze. This class takes an existing gamestate as input, and outputs an array representing the board and a set of features that it extracts from the gamestate.

**miner.py and miner2.py** are used for extracting dataframes of such arrays from game strings. Miner2.py should ideally break the whole games.csv file into a new csv where every position is mapped to a gamestate/row.

miner.py can be used to return a whole game from one row of data.

playbasicgame.py is intended to simulate playing a game of chess in the command line. Requires a working model.pikl file in the data folder.

models.py contains a forestmodel class, that can be trained on a full dataframe, or loaded from a valid pikl.

simple_search performs a depth=1 search of possible game states, and uses the model to score them, returning the gamestate that it judges to be the best next move.

print_board contains a function to print a representation of the game board from a row of pandas game data.
