# This is a sample Python script.
"""
this for handing input and displaying current GameState
"""

import pygame as p

import DoggemEngine
import SmartMoveFinder

DIMENSION = 4
SQ_SIZE = 60
WIDTH = HEIGHT = SQ_SIZE * DIMENSION + SQ_SIZE
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
    # this response are in game
    running = True
    # this response state endgame
    game_over = False
    # this response StartBoard
    startGameWith = True
    sqSelected = ()
    playerClicks = []
    PlayerOne = True  # if human play white this = true.If AI play this = false
    PlayerTwo = False  # revert previous comment. this can be play in 2 player if both playerOne and PlayerTwo are True
    while startGameWith:
        labelFont = p.font.SysFont("monospace", 18)
        whiteplay = labelFont.render("Play First", True, p.Color("black"))
        screen.blit(whiteplay, p.Rect(SQ_SIZE / 2, HEIGHT / 2, SQ_SIZE, SQ_SIZE))
        blackplay = labelFont.render("Play Last", True, p.Color("black"))
        screen.blit(blackplay, p.Rect(WIDTH - (2 * SQ_SIZE), HEIGHT / 2, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]
                row = location[1]
                if (SQ_SIZE / 2) <= col <= (3 * SQ_SIZE / 2) and (HEIGHT / 2) <= row <= (HEIGHT / 2 + SQ_SIZE):
                    startGameWith = False
                elif (WIDTH - (2 * SQ_SIZE)) <= col <= (WIDTH - SQ_SIZE) and (HEIGHT / 2) <= row <= (HEIGHT / 2 + SQ_SIZE):
                    PlayerTwo = True
                    PlayerOne = False
                    startGameWith = False
                    # clean background color left
                    screen.fill(p.Color("white"))
    while running:
        ''' control when game over reset map with similar config at start'''
        if game_over:
            screen.fill(p.Color("white"))
            gs = DoggemEngine.GameState()
            validMoves = gs.getValidMoves()
            sqSelected = ()
            playerClicks = []
            MoveMade = False
            game_over = False
        ''' check if this are humanTurn when play with AI '''
        humanTurn = (gs.whiteToMove and PlayerOne) or (not gs.whiteToMove and PlayerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE - 1
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    elif gs.whiteToMove and col > DIMENSION - 1:
                        sqSelected = ()
                        playerClicks = []
                    elif not gs.whiteToMove and row > DIMENSION - 1:
                        sqSelected = ()
                        playerClicks = []
                    elif len(playerClicks) == 0 and (col > DIMENSION - 1 or row > DIMENSION - 1):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = DoggemEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getDoggemNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            MoveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if humanTurn:
                        gs.undoMove()
                        gs.undoMove()
                    else:
                        gs.undoMove()
                    MoveMade = True
                if e.key == p.K_r:
                    gs = DoggemEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    MoveMade = False
        # AI move finder
        if not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves, 4)
            gs.makeMove(AIMove)
            MoveMade = True
        if MoveMade:
            validMoves = gs.getValidMoves()
            MoveMade = False
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        if gs.checkEndGame():
            game_over = True
            turnWin = "BLACK WIN" if gs.whiteToMove else "WHITE WIN"
            show_go_screen(screen, turnWin, running)
        elif len(validMoves) == 0:
            game_over = True
            show_go_screen(screen, "DRAW!", running)


'''
Highlight square select and move for piece selected
'''


def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE))
            # highlight move from that square
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow + SQ_SIZE))


'''
responsible for all the graphic within a current state
'''


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


'''
draw the squares on the board
'''


def drawBoard(screen):
    # colors = [p.Color("white"), p.Color("gray")]
    colors = [p.Color(238, 238, 210), p.Color(118, 150, 86)]
    blankcolors = p.Color("white")
    for r in range(DIMENSION):
        '''this clean move highlight left on blank column '''
        p.draw.rect(screen, blankcolors, p.Rect((DIMENSION + 1) * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE, SQ_SIZE, SQ_SIZE))
            '''this clean move highlight left on blank row  '''
            p.draw.rect(screen, blankcolors, p.Rect(c * SQ_SIZE, 0, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGE[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''this draw endgame screen'''


def show_go_screen(screen, turnWin, running):
    waiting = True
    screen.fill(p.Color("white"))
    TitleFont = p.font.SysFont("monospace", 40)
    labelFont = p.font.SysFont("monospace", 15)
    # render text
    labelTitle = TitleFont.render(turnWin, True, p.Color("black"))
    screen.blit(labelTitle, (SQ_SIZE / 2, HEIGHT / 4))
    labelReset = labelFont.render("press any key to reset board", True, p.Color("black"))
    screen.blit(labelReset, (SQ_SIZE / 2, HEIGHT / 4 + 50))
    clock = p.time.Clock()
    p.display.flip()
    while waiting:
        clock.tick(MAX_FPS)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                waiting = False


if __name__ == '__main__':
    main()
