import threading

import gui
import bot_process

def start_gui():
    gui.main()

def start_bot():
    bot_process.main()

def main():
    thread1 = threading.Thread(target=start_gui)
    thread1.start()
    thread2 = threading.Thread(target=start_bot)
    while bot_process.isEnd == False:
        if gui.isStart == True:
            thread2.start()
            gui.isStart = False


if __name__ == '__main__':
    main()