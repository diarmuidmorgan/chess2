import pandas as pd
def display(row):
    board = row_to_board(row)
    '''prints a visual represenation of the board'''
    #the representation is upside down
    string = '       A    B    C    D    E    F    G        '

    keys = {0:'_', 1:'P', 3:'N',4:'B',5:'R',9:'Q', 1000:'K'}




    for x in range(len(board)-1,-1,-1):

        string += '\n\n\n  '+str(x+1)+'  '
        for y in range(len(board[x])-1,-1,-1):

            if board[x][y]>0:

                string += '  '+keys[board[x][y]]+ '  '
            else:
                string += '  '+keys[abs(board[x][y])].lower() + '  '

    print(string)


def row_to_board(row):
    board=[]
    for x in range(0,8):
        board.append([])

        for y in range(0,8):

            board[x].append(row[str(x)+str(y)])

    return board
