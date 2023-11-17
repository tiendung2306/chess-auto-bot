import threading

import gui
import bot_process
import calibrate

def start_gui():
    gui.main()

def start_bot():
    bot_process.main()

def start_calibrate():
    calibrate.main()

def main():
    thread1 = threading.Thread(target=start_gui)
    thread1.start()
    thread2 = threading.Thread(target=start_bot)
    thread3 = threading.Thread(target=start_calibrate)
    thread3.start()
    while bot_process.isEnd == False:
        if gui.isStart == True:
            thread2.start()
            gui.isStart = False


if __name__ == '__main__':
    main()