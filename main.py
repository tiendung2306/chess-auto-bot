import pyautogui as pag
from PIL import Image
import time

WHITE = 1
BLACK = 0

side = WHITE #1 neu ban choi quan trang, 0 neu ban choi quan den
rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
cols = ['1', '2', '3', '4', '5', '6', '7', '8']

currChesboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                 ]

moveCount = 0

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
    x1 = click_piece(x)
    time.sleep(0.05)
    x2 = click_piece(y)
    currChesboard[x2[0]][x2[1]] = currChesboard[x1[0]][x1[1]]
    currChesboard[x1[0]][x1[1]] = ' '

def BotMovePiece(x="", y=""): #di tu x den y
    global currChesboard
    x1 = SquareNameToCoordinate(x)
    x2 = SquareNameToCoordinate(y)
    #di tu x1 den x2
    currChesboard[x2[0]][x2[1]] = currChesboard[x1[0]][x1[1]]
    currChesboard[x1[0]][x1[1]] = ' '


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
    if currChesboard[col][row] == ' ':
        return -1 #o do khong chua quan co nao
    if currChesboard[col][row] == 'r' or currChesboard[col][row] == 'n' or currChesboard[col][row] == 'b' or currChesboard[col][row] == 'q' or currChesboard[col][row] == 'k' or currChesboard[col][row] == 'p':
        return BLACK
    else:
        return WHITE

def Test():
    global moveCount, currChessboardPixel, prevChessboardPixel, currChesboard
    tmp = 0
    while True:
        if tmp == 5:
            break
        if moveCount % 2 == 1 - side:
            x = rows[tmp]
            move_piece(x + '2', x + '3')
            moveCount += 1
            tmp += 1
            for x in currChesboard:
                print(x, end='\n')
            print()
            time.sleep(0.5)
            prevChessboardPixel = getChessboardState()
        else:
            isMove = False
            time.sleep(1)
            botMoves = list()
            currChesboardPixel = getChessboardState()
            for i in range(0, 64):
                if prevChessboardPixel[i] != currChesboardPixel[i]:
                    x = i % 8
                    y = i // 8
                    squarename = CoordinateToSquareName(x, y)
                    if squarename != (rows[tmp-1] + '2') and squarename != (rows[tmp-1] + '3'):
                        print(squarename)
                        botMoves.append(squarename)
                        isMove = True
            if isMove :
                moveCount += 1
                if len(botMoves) != 2:
                    print('Panik!!!!!!!!!!!!!!!!!!!!!!!!!!')
                else:
                    if getChessSide(botMoves[0]) == 1 - side:
                        BotMovePiece(botMoves[0], botMoves[1])
                    else:
                        BotMovePiece(botMoves[1], botMoves[0])
                for x in currChesboard:
                    print(x, end='\n')
                print()

        # time.sleep(4)

def main():
    global piece_box_width, piece_box_height, chessboard_surface
    setup()
    # move_piece('d7', 'd5')
    chessboard_surface = (topleft_position[0], topleft_position[1], int(piece_box_width * 8), int(piece_box_height * 8))
    prevChessboardPixel = [(0, 0, 0)] * 64
    currChessboardPixel = [(0, 0, 0)] * 64
    global PrevImg, CurrImg
    global prevLegitChessboardPixel, currLegitChessboardPixel
    # prevLegitChessboardPixel = getChessboardState()
    # currLegitChessboardPixel = prevLegitChessboardPixel.copy()
    # prevChessboardPixel = prevLegitChessboardPixel.copy()
    # while True:
    #     currChessboardPixel = getChessboardState()
    #     if currChessboardPixel == prevChessboardPixel:
    #         prevLegitChessboardPixel = currLegitChessboardPixel.copy()
    #         currLegitChessboardPixel = currChessboardPixel.copy()
    #         for i in range(0, 64):
    #             if prevLegitChessboardPixel[i] != currLegitChessboardPixel[i]:
    #                 x = i % 8
    #                 y = i // 8
    #                 print(CoordinateToSquareName(x, y))
    #     prevChessboardPixel = currChessboardPixel.copy()
    #     time.sleep(0.15)

    Test()

    

if __name__ == "__main__":
    main()

