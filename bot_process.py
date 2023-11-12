import pyautogui as pag
from PIL import Image
from pynput.mouse import Listener
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
white_pawn_pixel = (0, 0, 0)

moveCount = 0
moves = ''

isEnd = False
delay_mode = True
#stockfish stats
skill_level = 4
movetime = 0.25

def setup():
    global side
    # global topleft_position
    # topleft_position = pag.locateOnScreen('Assets\\chess_com\\br_topleftpiece.png', minSearchTime=0.75)
    # if topleft_position == None:
    #     side = BLACK
    #     topleft_position = pag.locateOnScreen('Assets\\chess_com\\wr_topleftpiece.png', minSearchTime=0.75)
    # # print(topleft_position)
    # global botright_position
    # if side == WHITE:
    #     botright_position = pag.locateOnScreen('Assets\\chess_com\\wr_botrightpiece.png', minSearchTime=0.75)
    # else:
    #     botright_position = pag.locateOnScreen('Assets\\chess_com\\br_botrightpiece.png', minSearchTime=0.75)
    # # print(botright_position)
    # global piece_box_width
    # piece_box_width = (pag.center(botright_position)[0] - pag.center(topleft_position)[0])/7
    # global piece_box_height
    # piece_box_height = (pag.center(botright_position)[1] - pag.center(topleft_position)[1])/7
    global PrevImg, CurrImg
    PrevImg = pag.screenshot('Assets\\chess_com\\PrevScreen.png')
    CurrImg = pag.screenshot('Assets\\chess_com\\CurrScreen.png')

    f = open("settings.txt", "r")
    h3square_coord = f.readlines()
    h3square_coord = [int(i) for i in h3square_coord]
    # print(h3square_coord)
    f.close()   



    global topleft_position, botright_position
    topleft_position = (h3square_coord[0] - h3square_coord[2] * 7, h3square_coord[1] - h3square_coord[3] * 5, h3square_coord[2], h3square_coord[3])
    botright_position = (h3square_coord[0], h3square_coord[1] + h3square_coord[3] * 2, h3square_coord[2], h3square_coord[3])

    global piece_box_width
    piece_box_width = (pag.center(botright_position)[0] - pag.center(topleft_position)[0])/7
    global piece_box_height
    piece_box_height = (pag.center(botright_position)[1] - pag.center(topleft_position)[1])/7

    h3squarecenter = pag.center(h3square_coord)
    if CurrImg.getpixel((h3squarecenter[0], h3squarecenter[1] + h3square_coord[3])) == white_pawn_pixel:
        side = WHITE
    else: 
        side = BLACK
    
    print(side)

    sf.Init(skill_level)
    setCurrChessboard()

def is_clicked(x, y, button, pressed):
    global h3pos
    if pressed:
        print(x, ' ', y, ' Clicked ! ') #in your case, you can move it to some other pos
        h3pos = (x, y)
        return False # to stop the thread after click

def check_click():
    with Listener(on_click=is_clicked) as listener:
        listener.join()

def calibrate():
    global white_square_pixel, black_square_pixel, white_pawn_pixel
    #nguoi dung se click vao o h3(mau trang)
    check_click()
    CalibrateImg = pag.screenshot('Assets\\chess_com\\CalibrateScreen.png')
    h3pixel = CalibrateImg.getpixel(h3pos)
    #find leftmost h3
    h3pos_tmp = h3pos
    k = 0
    while(CalibrateImg.getpixel((h3pos_tmp[0] - k, h3pos_tmp[1])) == h3pixel):
        k += 1
    h3left = h3pos_tmp[0] - k + 1
    #find rightmost h3
    k = 0
    while(CalibrateImg.getpixel((h3pos_tmp[0] + k, h3pos_tmp[1])) == h3pixel):
        k += 1
    h3right = h3pos_tmp[0] + k - 1
    #find topmost h3
    k = 0
    while(CalibrateImg.getpixel((h3pos_tmp[0], h3pos_tmp[1] - k)) == h3pixel):
        k += 1
    h3top = h3pos_tmp[1] - k + 1
    #find botmost h3
    k = 0
    while(CalibrateImg.getpixel((h3pos_tmp[0], h3pos_tmp[1] + k)) == h3pixel):
        k += 1
    h3bot = h3pos_tmp[1] + k - 1
    h3square_coord = (h3left, h3top, h3right - h3left, h3bot - h3top)
    white_square_pixel = h3pixel
    black_square_pixel = CalibrateImg.getpixel((h3left - 1, h3top))
    h3squarecenter = pag.center(h3square_coord)
    white_pawn_pixel = CalibrateImg.getpixel((h3squarecenter[0], h3squarecenter[1] + h3square_coord[3]))
    f = open("settings.txt", "w")
    for i in range(4):
        f.write(str(h3square_coord[i]) + '\n')
    f.close()

def setCurrChessboard():
    global currChessboard
    if side == BLACK:
        for i in range(0, 64):
            x = i % 8
            y = i // 8
            currChessboard[y][7-x] = sf.GetPiece(i)
    else:
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

def make_delay():
    tmp = random.randint(0, 100)
    if tmp < 8 == 0:
        time.sleep(random.randint(10, 20)) #chinh delay giua moi lan minh di mot nuoc
    elif tmp < 50:
        time.sleep(random.randint(4, 7)) #chinh delay giua moi lan minh di mot nuoc
    else:
        time.sleep(random.randint(0, 3)) #chinh delay giua moi lan minh di mot nuoc

def move_piece(x="", y="", z=None): #di chuyen quan co tu o x den o y, neu z != None thi nuoc di do la phong quan, va quan duoc phong la z
    global moves, delay_mode
    delay_time_btw_2click = 0.1
    if delay_mode == True:
        make_delay()
    if z == None:
        x1 = click_piece(x)
        time.sleep(delay_time_btw_2click)
        x2 = click_piece(y)
        moves += x + y + ' '
        sf.Move(x + y)
    else: #nuoc di vua roi la nuoc phong quan
        x1 = click_piece(x)
        time.sleep(delay_time_btw_2click)
        x2 = click_piece(y)
        time.sleep(delay_time_btw_2click)
        if z == 'q' or z == 'Q': #phong hau
            click_piece(y)
        elif z == 'n' or z == 'N': #phong ma
            if side == WHITE:
                y = y[0] + str(int(y[1]) - 1)
            else:
                y = y[0] + str(int(y[1]) + 1)
            click_piece(y)
        elif z == 'r' or z == 'R': #phong xe
            if side == WHITE:
                y = y[0] + str(int(y[1]) - 2)
            else:
                y = y[0] + str(int(y[1]) + 2)
            click_piece(y)
        elif z == 'b' or z == 'B': #phong tuong
            if side == WHITE:
                y = y[0] + str(int(y[1]) - 3)
            else:
                y = y[0] + str(int(y[1]) + 3)
            click_piece(y)
        else:
            print('WTF the la no phong quan gi?????')
        
        sf.Move(x + y + z)
        moves += x + y + z + ' '
    setCurrChessboard()

def EnemyMovePiece(x="", y=""): #di tu x den y
    global currChessboard, moves, side
    x1 = SquareNameToCoordinate(x)
    x2 = SquareNameToCoordinate(y)
    #kiem tra neu o x1 la con tot va o x2 la o cuoi bang
    if (currChessboard[x1[0]][x1[1]] == 'p' or currChessboard[x1[0]][x1[1]] == 'P') and ((side == WHITE and y[1] == '1') or (side == BLACK and y[1] == '8')):
        moves += x + y + 'q' + ' '
        sf.Move(x + y + 'q')
    else:
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
    global currChessboard
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

    # print(currChessboard)

    if side == BLACK: #neu minh choi quan den
        isEnemyMove = False
        while isEnemyMove == False:
            tmpChessboardPixel = getChessboardState()
            for i in range(0, 64):
                x = i % 8
                y = i // 8
                if y > 1 and y < 6:
                    if (x + y) % 2 == 0:
                        if tmpChessboardPixel[i] != white_square_pixel:
                            move2 = CoordinateToSquareName(x, y)
                            isEnemyMove = True
                    else:
                        if tmpChessboardPixel[i] != black_square_pixel:
                            move2 = CoordinateToSquareName(x, y)
                            isEnemyMove = True
                else:
                    if (x + y) % 2 == 0:
                        if tmpChessboardPixel[i] == white_yellow_square_pixel:
                            move1 = CoordinateToSquareName(x, y)
                    else:
                        if tmpChessboardPixel[i] == black_yellow_square_pixel:
                            move1 = CoordinateToSquareName(x, y)
        EnemyMovePiece(move1, move2)
        moveCount += 1


    while sf.isGameOver() == False:
        global myMove1, myMove2
        if isEnd == True:
            sf.QuitEngine()
            exit()
        if moveCount % 2 == 1 - side: #den luot minh di chuyen
            move = sf.GetNextMove(movetime)
            if len(move) == 4:
                myMove1 = move[0] + move[1]
                myMove2 = move[2] + move[3]
                move_piece(myMove1, myMove2)
            elif len(move) == 5: #phong quan
                print('It\'s timeeeeeeeee, my little pawn')
                myMove1 = move[0] + move[1]
                myMove2 = move[2] + move[3]
                move_piece(myMove1, myMove2, move[4])
            else:
                print('Panikkkkkkkkkk')
            moveCount += 1
            # for x in currChessboard:
            #     print(x, end='\n')
            # print()
            time.sleep(0.025)
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
                        print('What the hell????')
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

