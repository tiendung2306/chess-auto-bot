from tkinter import *
from tkinter import messagebox
import time

import bot_process
import calibrate

isStart = False
isCalibrate = False
state_text = 'waiting..'
isEnd = False
isMenu = True

def update_state_text():
    if isCalibrate:
        state_text = 'calibrating..'
    elif isStart == False:
        state_text = 'waiting..'    
    else:
        state_text = 'running..'    
    state_label.config(text=state_text)

def start():
    global isStart
    isStart = True
    bot_process.isRestart = False
    bot_process.isStart = True
    update_state_text()

def change_delaymode():
    global delaymode_btn
    bot_process.delay_mode = not bot_process.delay_mode
    if bot_process.delay_mode:
        state = 'On'
    else:
        state = 'Off'
    delaymode_btn.config(text='DelayMode: ' + state)

def calibrate():
    global state_text, isCalibrate, state_label
    isCalibrate = not isCalibrate
    update_state_text()
    
def change_mode():
    global mode_btn
    bot_process.mode = 1 - bot_process.mode
    if bot_process.mode == bot_process.CHESS_COM:
        state = 'chess.com'
    else:
        state = 'lichess.org'
    mode_btn.config(text='Mode: ' + state)

def restart():
    global isStart
    bot_process.isRestart = True
    state_label.config(text='restarting..')
    isStart = False
    root.after(3000, update_state_text)

def quit():
    global root, isEnd
    bot_process.isEnd = True
    isEnd = True
    root.destroy()
    
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        quit()



def main():
    global isStart, root, state_text, state_label, delaymode_btn, mode_btn
    isStart = False
    root = Tk()
    root.title('Chess auto bot')
    root.geometry("")
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    Button(root, text='Calibrate', font=('Arial', 18), command=calibrate).grid(row=0, column=0)
    mode_btn = Button(root, text='Mode: chess.com', font=('Arial', 16), command=change_mode)
    mode_btn.grid(row=0, column=1)
    state_label = Label(root, text=state_text, font=('Arial', 24))
    state_label.grid(row=1, column=0)
    Button(root, text='Start', font=('Arial', 18), command=start).grid(row=2, column=0)
    Button(root, text='Restart', font=('Arial', 18), command=restart).grid(row=2, column=1)
    delaymode_btn = Button(root, text='DelayMode: On', font=('Arial', 18), command=change_delaymode)
    delaymode_btn.grid(row=3, column=0)
    Button(root, text='Quit', font=('Arial', 18), command=quit).grid(row=3, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()

