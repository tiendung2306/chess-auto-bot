from tkinter import *
from tkinter import ttk
import os

import bot_process

isStart = False
isCalibrate = False
state_text = 'running..'

def fun():
    if isStart:
        bot_process.main()

def start():
    global isStart
    isStart = True

def stop():
    pass

def calibrate():
    global state_text, isCalibrate, state_label
    isCalibrate = not isCalibrate
    if isCalibrate:
        state_text = 'calibrating..'
    else:
        state_text = 'running..'
    state_label.config(text=state_text)
    bot_process.calibrate()
    

def quit():
    global root
    root.destroy()
    bot_process.isEnd = True

def main():
    global isStart, root, state_text, state_label
    isStart = False
    root = Tk()
    root.title('Chess auto bot')
    root.geometry('230x230')
    root.attributes('-topmost', True)

    Button(root, text='Calibrate', font=('Arial', 18), command=calibrate).grid(row=0, column=0)
    state_label = Label(root, text=state_text, font=('Arial', 24))
    state_label.grid(row=1, column=0)
    Button(root, text='Start', font=('Arial', 18), command=start).grid(row=2, column=0)
    Button(root, text='Pause', font=('Arial', 18), command=stop).grid(row=3, column=0)
    Button(root, text='Quit', font=('Arial', 18), command=quit).grid(row=4, column=2)

    root.mainloop()

if __name__ == '__main__':
    main()

