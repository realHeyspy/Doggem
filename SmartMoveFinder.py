import random
import numpy as np
import copy

'''AI move randomly'''


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''AI with minimax'''


def findBestMove(gs, validMoves, depth):
    turn = "wp" if gs.whiteToMove else "bp"
    compareBoard = DoggemMinMax(gs.getSizeBoard(), turn)
    compareBoard.createBoxCompare(gs.getSizeBoard())
    return compareBoard.minimax(gs, validMoves, depth)


class DoggemMinMax():
    def __init__(self, inputSize, turn):
        self.currentSize = inputSize * inputSize
        self.maxInt = self.currentSize * 5 - 5
        self.whiteBox = [1] * self.currentSize
        self.blackBox = [1] * self.currentSize
        self.turn = turn
        self.currentUnitBoard = inputSize - 1

    # create compare Box automatic
    def createBoxCompare(self, inputSize):
        value = 0
        count = 0
        i = inputSize * (inputSize - 1)
        while count != self.currentSize:
            if (i + 1) % inputSize == 0:
                self.whiteBox.__setitem__(i, value)
                value += 5
                i -= (inputSize * 2 - 1)
                count += 1
            else:
                self.whiteBox.__setitem__(i, value)
                value += 5
                i += 1
                count += 1
        value = count = 0
        i = j = inputSize * (inputSize - 1)
        while count != self.currentSize:
            if (j - inputSize) < 0:
                self.blackBox.__setitem__(j, value)
                value -= 5
                j = i + 1
                i += 1
                count += 1
            else:
                self.blackBox.__setitem__(j, value)
                value -= 5
                j -= inputSize
                count += 1

    def eval(self, board):
        evalPoint = 0
        currentWhiteInBoard = self.currentUnitBoard
        currentBlackInBoard = self.currentUnitBoard
        checkBoard = np.ravel(board)
        for i in range(self.currentSize):
            if checkBoard[i] == "wp":
                currentWhiteInBoard -= 1
                evalPoint += self.whiteBox[i]
                check = i - 3
                while check >= 0:
                    if checkBoard[i] == "bp":
                        downPoint = (i - check - 1) / 3 * 10
                        evalPoint -= (self.maxInt - downPoint)
                    check -= 3
            if checkBoard[i] == "bp":
                currentBlackInBoard -= 1
                evalPoint += self.blackBox[i]
                check = i + 1
                while check % self.currentSize != 0:
                    if checkBoard[check] == "wp":
                        downPoint = 10 * (check - i - 1)
                        evalPoint += self.maxInt - downPoint
                    check += 1
        evalPoint += currentWhiteInBoard * (self.maxInt + 10) * 8
        evalPoint -= currentBlackInBoard * (self.maxInt + 10) * 8
        return evalPoint

    # check if this was end game board
    def IsEndBoard(self, board):
        currentWhiteInBoard = self.currentUnitBoard
        currentBlackInBoard = self.currentUnitBoard
        for i in range(self.currentSize):
            if board[i] == "wp":
                currentWhiteInBoard -= 1
            if board[i] == "bp":
                currentBlackInBoard -= 1
            return True if currentBlackInBoard == 0 or currentBlackInBoard == 0 else False

    def minVal(self, board, depth, turned):
        currentTurn = "bp" if turned == "wp" else "wp"
        if depth == 0 or self.IsEndBoard(board):
            return self.eval(board)
        else:
            FutureBoard = self.FutureChangeBoard(board, currentTurn)
            minVals = []
            minInt = 1000000
            for futureStatesBoard in FutureBoard:
                minVals.append(self.maxVal(futureStatesBoard, depth - 1, currentTurn))
            for i in minVals:
                if i < minInt:
                    minInt = i
            return minInt

    def maxVal(self, board, depth, turned):
        currentTurn = "bp" if turned == "wp" else "wp"
        if depth == 0 or self.IsEndBoard(board):
            return self.eval(board)
        else:
            FutureBoard = self.FutureChangeBoard(board, currentTurn)
            maxVals = []
            maxInt = -1000000
            for futureStatesBoard in FutureBoard:
                maxVals.append(self.minVal(futureStatesBoard, depth - 1, currentTurn))
            for i in maxVals:
                if i > maxInt:
                    maxInt = i
            return maxInt

    def minimax(self, gs, validMoves, depth):
        bestMove = None
        turned = True if self.turn == "wp" else False
        vals = -1000000 if turned else 1000000
        # same unit ai play
        for move in validMoves:
            board = Board(gs.board, (move.startRow, move.startCol), (move.endRow, move.endCol)).getBoard()
            if turned:
                maxval = self.maxVal(board, depth - 1, "wp")
                if vals <= maxval:
                    vals = maxval
                    bestMove = move
            else:
                minval = self.minVal(board, depth - 1, "bp")
                if vals >= minval:
                    vals = minval
                    bestMove = move
        return bestMove

    '''
    Main process future move for minimax
    '''

    def FutureChangeBoard(self, currentBoard, currentTurn):
        board = []
        currentSize = len(currentBoard)
        for r in range(len(currentBoard)):
            for c in range(len(currentBoard[r])):
                turn = currentBoard[r][c]
                if turn == 'wp' and turn == currentTurn:  # white move
                    self.FutureWhitePawnMoves(r, c, board, currentBoard, currentSize)
                elif turn == 'bp' and turn == currentTurn:  # black move
                    self.FutureBlackPawnMoves(r, c, board, currentBoard, currentSize)
        return board

    '''future white AI move'''

    def FutureWhitePawnMoves(self, r, c, board, currentBoard, currentSize):
        whitePawnMove = ((0, -1), (-1, 0), (0, 1))
        for m in whitePawnMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if -1 <= endRow < currentSize and 0 <= endCol < currentSize:
                endPiece = currentBoard[endRow][endCol]
                if endPiece == '--':
                    board.append(Board(currentBoard, (r, c), (endRow, endCol)).getBoard())

    '''future black AI move'''

    def FutureBlackPawnMoves(self, r, c, board, currentBoard, currentSize):
        blackPawnMove = ((1, 0), (-1, 0), (0, 1))
        for m in blackPawnMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < currentSize and 0 <= endCol <= currentSize:
                if endCol == currentSize:
                    endCol = -1
                    endPiece = "--"
                else:
                    endPiece = currentBoard[endRow][endCol]
                if endPiece == "--":
                    board.append(Board(currentBoard, (r, c), (endRow, endCol)).getBoard())


class Board():
    """ deepcopy need to game status board don't change"""

    def __init__(self, currentBoard, startSq, endSq):
        startRow = startSq[0]
        startCol = startSq[1]
        endRow = endSq[0]
        endCol = endSq[1]
        if endRow == -1 or endCol == len(currentBoard):
            self.pieceMoved = "--"
        else:
            self.pieceMoved = currentBoard[startRow][startCol]
        self.pieceCaptured = currentBoard[endRow][endCol]
        self.board = copy.deepcopy(currentBoard)
        self.board[startRow][startCol] = self.pieceCaptured
        self.board[endRow][endCol] = self.pieceMoved

    '''return board from Move object'''

    def getBoard(self):
        return self.board
