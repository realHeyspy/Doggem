# This is a sample Python script.
"""
this for handing input and displaying current GameState
"""

import pygame as p
import DoggemEngine

WIDTH = HEIGHT = 240
DIMENSION = 4
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGE = {}


def loadImage():
    IMAGE['bp'] = p.transform.scale(p.image.load("imageUnit/bp.png"), (SQ_SIZE, SQ_SIZE))
    IMAGE['wp'] = p.transform.scale(p.image.load("imageUnit/wp.png"), (SQ_SIZE, SQ_SIZE))


def main():
    gs = DoggemEngine.GameState()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    validMoves = gs.getValidMoves()
    MoveMade = False
    loadImage()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = DoggemEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # print(move.getDoggemNotation())
                    if move in validMoves:  # error here validMoves null
                        gs.makeMove(move)
                        MoveMade = True
                    sqSelected = ()  # reset user clicks
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    MoveMade = True
        if MoveMade:
            validMoves = gs.getValidMoves()
            MoveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
responsible for all the graphic within a current state
'''


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


'''
draw the squares on the board
'''


def drawBoard(screen):
    # colors = [p.Color("white"), p.Color("gray")]
    colors = [p.Color(238, 238, 210), p.Color(118, 150, 86)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    pass
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGE[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
