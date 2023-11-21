import threading
import time

import gui
import bot_process
import calibrate

def start_gui():
    gui.main()

def start_bot():
    bot_process.start()

def start_calibrate():
    calibrate.main()

def main():
    thread1 = threading.Thread(target=start_gui)
    thread1.setDaemon(True)
    thread1.start()
    thread2 = threading.Thread(target=start_bot)
    thread2.setDaemon(True)
    thread3 = threading.Thread(target=start_calibrate)
    thread3.setDaemon(True)
    thread3.start()
    thread2.start()

    while True:
        time.sleep(1)
        # print('alive!!!')
        if not thread1.is_alive() or not thread2.is_alive() or not thread3.is_alive():
            return()


if __name__ == '__main__':
    main()