import numpy as np

"""
this class is responsible for storing all the information about current state 
"""
'''
error when move before append
'''


class GameState():
    def __init__(self):
        self.board = [
            ["bp", "--", "--", "--"],
            ["bp", "--", "--", "--"],
            ["bp", "--", "--", "--"],
            ["--", "wp", "wp", "wp"]]
        self.whiteToMove = True
        self.movelog = []
        self.currentSize = 4

    def changeBoard(self, number: int):
        for i in range(number * number):
            if i % number == 0 and i != (number * (number - 1)):
                self.board[i] = "bp"
            elif i > (number * (number - 1)):
                self.board[i] = "wp"
            else:
                self.board[i] = "--"
        self.board = np.reshape(self.board, (number, number))
        self.whitebox = []
        self.blackbox = []
        self.currentSize = number
        self.matrixSize = number * number
        self.maxInt = self.matrixSize * 5 - 5
        i = (number * (number - 1))
        value = count = 0
        while count != (number * number):
            if (i + 1) % number == 0:
                self.whitebox[i] = value
                value += 5
                i = i - (number * 2 - 1)
                count += 1
            else:
                self.whitebox[i] = value
                value += 5
                i += 1
                count += 1
        value = count = 0
        i = j = (number * (number - 1))
        while count != number * number:
            if j - number < 0:
                self.blackbox[j] = value
                value -= 5
                j = i + 1
                i += 1
                count += 1
            else:
                self.blackbox[j] = value
                value -= 5
                j -= number
                count += 1

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move)
            self.whiteToMove = not self.whiteToMove  # swap player

    '''Undo last move'''

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn move
            self.getWhitePawnMoves(r, c, moves)
        else:  # black pawn move
            self.getBlackPawnMoves(r, c, moves)

    '''
     step white pawn moves
     (#,#)         (-1,0)       (#,#)
     (0,-1)        (0,0)       (0,1)
     up right left
    '''

    def getWhitePawnMoves(self, r, c, moves):
        whitePawnMove = ((0, -1), (-1, 0), (0, 1))
        for m in whitePawnMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < self.currentSize and 0 <= endCol < self.currentSize:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--':
                    print("white units", self.whiteToMove)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
     step black pawn moves
     (#,#)        (1,0)       (#,#)
     (#,#)        (0,0)       (0,1)
     (#,#)        (-1,0)      (#,#)
     up right down
    '''

    def getBlackPawnMoves(self, r, c, moves):
        blackPawnMove = ((1, 0), (-1, 0), (0, 1))
        for m in blackPawnMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < self.currentSize and 0 <= endCol < self.currentSize:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    print("black units", self.whiteToMove)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    rankToRows = {"1": 3, "2": 2, "3": 1, "4": 0}
    rowsToRank = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''Overriding equal move'''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getDoggemNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]
