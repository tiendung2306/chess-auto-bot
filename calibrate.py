import pyautogui as pag
import gui
import win32api


def check_click():
    global h3pos
    while True:
        if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
            print(pag.position())
            h3pos = pag.position()
            return
 
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
    for i in range(3):
        f.write(str(white_pawn_pixel[i]) + '\n')
    f.close()

def main():
    while gui.isEnd == False:
        if gui.isCalibrate:
            calibrate()
            gui.isCalibrate = False
            gui.update_state_text()

if __name__ == '__main__':
    main()

    