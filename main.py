import pyautogui as pag

WHITE = 1
BLACK = 0

side = WHITE #1 neu ban choi quan trang, 0 neu ban choi quan den
rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
cols = ['1', '2', '3', '4', '5', '6', '7', '8']

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
    
def move_piece(x="", y=""): #di chuyen quan co tu o x den o y
    click_piece(x)
    click_piece(y)

if __name__ == "__main__":
    setup()
    move_piece('b4', 'c3')