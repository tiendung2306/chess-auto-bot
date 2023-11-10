import pyautogui as pag
from PIL import Image
import time

import stockfish as sf

import random

WHITE = 1
BLACK = 0

side = WHITE #1 neu ban choi quan trang, 0 neu ban choi quan den
rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
cols = ['1', '2', '3', '4', '5', '6', '7', '8']

currChessboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                 ]

black_square_pixel = (119, 153, 84)
white_square_pixel = (233, 237, 204)
black_yellow_square_pixel = (187, 204, 68)
white_yellow_square_pixel = (244, 246, 128)

moveCount = 0
moves = ''

delay_mode = True
#stockfish stats
skill_level = 5
movetime = 0.2

def setup():
    global side
    global topleft_position
    topleft_position = pag.locateOnScreen('Assets\\chess_com\\br_topleftpiece.png', minSearchTime=0.75)
    if topleft_position == None:
        side = BLACK
        topleft_position = pag.locateOnScreen('Assets\\chess_com\\wr_topleftpiece.png', minSearchTime=0.75)
    # print(topleft_position)
    global botright_position
    if side == WHITE:
        botright_position = pag.locateOnScreen('Assets\\chess_com\\wr_botrightpiece.png', minSearchTime=0.75)
    else:
        botright_position = pag.locateOnScreen('Assets\\chess_com\\br_botrightpiece.png', minSearchTime=0.75)
    # print(botright_position)
    global piece_box_width
    piece_box_width = (pag.center(botright_position)[0] - pag.center(topleft_position)[0])/7
    global piece_box_height
    piece_box_height = (pag.center(botright_position)[1] - pag.center(topleft_position)[1])/7
    global PrevImg, CurrImg
    PrevImg = pag.screenshot('Assets\\chess_com\\PrevScreen.png')
    CurrImg = pag.screenshot('Assets\\chess_com\\CurrScreen.png')

    sf.Init(skill_level)
    setCurrChessboard()

def setCurrChessboard():
    global currChessboard
    for i in range(0, 64):
        x = i % 8
        y = i // 8
        currChessboard[y][7-x] = sf.GetPiece(63 - i)


def click_piece(x=""):
    row = 0
    col = 0
    for i in range(0, 8):
        if rows[i] == x[0]:
            row = i
    if side == BLACK:
        col = int(x[1]) - 1
        row = 7 - row
    else:
        col = 8 - int(x[1])
    pag.click(pag.center(topleft_position)[0] + piece_box_width * row, pag.center(topleft_position)[1] + piece_box_height * col)
    return (col, row)
    
def CoordinateToSquareName(x, y):
    if side == WHITE:
        row = rows[x]
        col = cols[7-y]
    else:
        row = rows[7-x]
        col = cols[y]
    return row + col

def SquareNameToCoordinate(x=""):
    row = 0
    col = 0
    for i in range(0, 8):
        if rows[i] == x[0]:
            row = i
    if side == BLACK:
        col = int(x[1]) - 1
        row = 7 - row
    else:
        col = 8 - int(x[1])
    return (col, row)

def move_piece(x="", y=""): #di chuyen quan co tu o x den o y
    global moves, delay_mode
    if delay_mode == True:
        time.sleep(random.randint(0, 10)) #chinh delay giua moi lan minh di mot nuoc
    x1 = click_piece(x)
    time.sleep(0.05)
    x2 = click_piece(y)
    moves += x + y + ' '
    sf.Move(x + y)
    
    setCurrChessboard()

def EnemyMovePiece(x="", y=""): #di tu x den y
    global currChessboard, moves, side
    x1 = SquareNameToCoordinate(x)
    x2 = SquareNameToCoordinate(y)
    #di tu x1 den x2
    moves += x + y + ' '
    sf.Move(x + y)

    setCurrChessboard()


def FindSquare(x):
    global side, topleft_position, botright_position, piece_box_width, piece_box_height
    y = pag.center(x)
    posX = abs(int((y[0] - topleft_position[0])//piece_box_width))
    posY = abs(int((y[1] - topleft_position[1])//piece_box_height))
    print(y[1], end=' ')
    return CoordinateToSquareName(posX, posY)

def GetCenterPixel(x, y):
    global PrevImg, CurrImg, topleft_position, piece_box_width, piece_box_height
    # pag.moveTo(pag.center(topleft_position)[0] + piece_box_width * x, pag.center(topleft_position)[1] + piece_box_height * y)
    return CurrImg.getpixel((pag.center(topleft_position)[0] + piece_box_width * x, pag.center(topleft_position)[1] + piece_box_height * y))

def getChessboardState():
    global CurrImg
    CurrImg = pag.screenshot('Assets\\chess_com\\CurrScreen.png')
    arr = [(0, 0, 0)] * 64
    for i in range(0, 64):
        x = i % 8
        y = i // 8
        # prevChessboardPixel[i] = GetCenterPixel(x, y, 0)
        arr[i] = GetCenterPixel(x, y)
    return arr

def getChessSide(x):
    (col, row) = SquareNameToCoordinate(x)
    if currChessboard[col][row] == ' ':
        return -1 #o do khong chua quan co nao
    if currChessboard[col][row] == 'r' or currChessboard[col][row] == 'n' or currChessboard[col][row] == 'b' or currChessboard[col][row] == 'q' or currChessboard[col][row] == 'k' or currChessboard[col][row] == 'p':
        return BLACK
    else:
        return WHITE

def Process():
    global moveCount, currChessboardPixel, prevChessboardPixel, currChessboard
    takeChessboardStateAgain = False

    print(currChessboard)

    if side == BLACK: #neu minh choi quan den
        tmpChessboardPixel = getChessboardState()
        for i in range(0, 64):
            x = i % 8
            y = i // 8
            if y > 1 and y < 6:
                if (x + y) % 2 == 0:
                    if tmpChessboardPixel[i] != white_square_pixel:
                        move2 = CoordinateToSquareName(x, y)
                else:
                    if tmpChessboardPixel[i] != black_square_pixel:
                        move2 = CoordinateToSquareName(x, y)
            else:
                if (x + y) % 2 == 0:
                    if tmpChessboardPixel[i] == white_yellow_square_pixel:
                        move1 = CoordinateToSquareName(x, y)
                else:
                    if tmpChessboardPixel[i] == black_yellow_square_pixel:
                        move1 = CoordinateToSquareName(x, y)
        EnemyMovePiece(move1, move2)
        moveCount += 1


    while True:
        global myMove1, myMove2
        if moveCount % 2 == 1 - side: #den luot minh di chuyen
            move = sf.GetNextMove(movetime)
            myMove1 = move[0] + move[1]
            myMove2 = move[2] + move[3]
            move_piece(myMove1, myMove2)
            moveCount += 1
            # for x in currChessboard:
            #     print(x, end='\n')
            # print()
            time.sleep(0.75)
            prevChessboardPixel = getChessboardState()
        else:
            isMove = False
            time.sleep(1.5)
            enemyMoves = list()
            currChessboardPixel = getChessboardState()
            for i in range(0, 64):
                if prevChessboardPixel[i] != currChessboardPixel[i]:
                    if takeChessboardStateAgain == False:
                        takeChessboardStateAgain = True
                        break
                    x = i % 8
                    y = i // 8
                    squarename = CoordinateToSquareName(x, y)
                    if squarename != myMove1 and squarename != myMove2:
                        # print(squarename)
                        enemyMoves.append(squarename)
                        isMove = True
            if len(enemyMoves) == 1:
                (x1, y1) = SquareNameToCoordinate(myMove1)
                (x2, y2) = SquareNameToCoordinate(myMove2)
                (xe, ye) = SquareNameToCoordinate(enemyMoves[0])
                if prevChessboardPixel[x1 * 8 + y1] == black_yellow_square_pixel or prevChessboardPixel[x1 * 8 + y1] == white_yellow_square_pixel:
                    if (x1 + y1) % 2 == 0: #o (x1, y1) la o mau` trang
                        if currChessboardPixel[x1 * 8 + y1] == white_square_pixel: #o hien tai la o trong
                            enemyMoves.append(myMove2)
                        else:
                            enemyMoves.append(myMove1)
                    else:
                        if currChessboardPixel[x1 * 8 + y1] == black_square_pixel: #o hien tai la o trong
                            enemyMoves.append(myMove2)
                        else:
                            enemyMoves.append(myMove1)
                else:
                    if (x2 + y2) % 2 == 0: #o (x2, y2) la o mau` trang
                        if currChessboardPixel[x2 * 8 + y2] == white_square_pixel: #o hien tai la o trong
                            enemyMoves.append(myMove1)
                        else:
                            enemyMoves.append(myMove2)
                    else:
                        if currChessboardPixel[x2 * 8 + y2] == black_square_pixel: #o hien tai la o trong
                            enemyMoves.append(myMove1)
                        else:
                            enemyMoves.append(myMove2)
            if isMove :
                takeChessboardStateAgain = False
                moveCount += 1
                if len(enemyMoves) != 2:
                    if len(enemyMoves) == 4:
                        for x in enemyMoves:
                            if x[0] == 'a': #nhap thanh dai
                                EnemyMovePiece('e' + x[1], 'a' + x[1])
                            elif x[0] == 'h': #nhap thanh ngan
                                EnemyMovePiece('e' + x[1], 'h' + x[1])
                    else:
                        print(enemyMoves)
                else:
                    if getChessSide(enemyMoves[0]) == 1 - side:
                        EnemyMovePiece(enemyMoves[0], enemyMoves[1])
                    elif getChessSide(enemyMoves[1]) == 1 - side:
                        EnemyMovePiece(enemyMoves[1], enemyMoves[0])
                    else:
                        print('What tf is going on????')
                        print(enemyMoves)
                        print(currChessboard)

def main():
    global piece_box_width, piece_box_height, chessboard_surface
    setup()
    # move_piece('d7', 'd5')
    chessboard_surface = (topleft_position[0], topleft_position[1], int(piece_box_width * 8), int(piece_box_height * 8))

    Process()
    sf.QuitEngine()


if __name__ == "__main__":
    main()

