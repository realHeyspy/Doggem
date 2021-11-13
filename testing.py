import numpy as np

"""
just for testing some thing not remember
"""
if __name__ == '__main__':
    board = [
        ["bp", "--", "--", "--"],
        ["bp", "--", "--", "--"],
        ["bp", "--", "--", "--"],
        ["--", "wp", "wp", "wp"]]
    for i in range(4):
        for j in range(4):
            print(str(i) + " " + str(j) + " result " + board[i][j])
    print(board[3][2])

    newBoard = np.reshape(board, (1, 16))
    print(newBoard)
