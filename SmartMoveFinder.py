import random
import numpy as np


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove():
    pass


class DoggemMinMax():
    def __init__(self):
        self.whiteBox = []
        self.blackBox = []

    def createBoxCompare(self, inputSize):
        value = 0
        count = 0
        i = inputSize * (inputSize - 1)
        while count != inputSize * inputSize:
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
        while count != inputSize * inputSize:
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
        whiteBox = np.reshape(self.whiteBox, (3, 3))
        blackBox = np.reshape(self.blackBox, (3, 3))