from tkinter import *
from tkinter import ttk
import os

import bot_process

isStart = False

def fun():
    if isStart:
        bot_process.main()

def start():
    global isStart
    isStart = True

def stop():
    pass

def quit():
    global root
    root.destroy()
    bot_process.isEnd = True

def main():
    global isStart, root
    isStart = False
    root = Tk()
    root.title('Chess auto bot')
    root.geometry('230x230')
    root.attributes('-topmost', True)

    Button(root, text='Calibrate', font=('Arial', 18)).grid(row=0, column=0)
    Label(root, text='running..', font=('Arial', 24)).grid(row=1, column=0)
    Button(root, text='Start', font=('Arial', 18), command=start).grid(row=2, column=0)
    Button(root, text='Pause', font=('Arial', 18), command=stop).grid(row=3, column=0)
    Button(root, text='Quit', font=('Arial', 18), command=quit).grid(row=4, column=2)

    root.mainloop()

if __name__ == '__main__':
    main()

