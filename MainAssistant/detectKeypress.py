import threading

import keyboard
import time
from MainAssistant import main
import subprocess as s



hotkey = "shift + alt"
Killhotkey = "ctrl + alt"
def killProcess(pid):
    s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
def kill():
    while True:
        if keyboard.is_pressed(Killhotkey):
            print("Killed")
            killProcess(main.PID)
        time.sleep(.5)
# Remember that the order in which the hotkey is set up is the order you
# need to press the keys.
x = threading.Thread(target = kill)
x.start()
while True:
    # if main.kill:
    #     sys.exit("Kill Executed")
    # if main.paused:
    #     continue
    if keyboard.is_pressed(hotkey):

        print("Hotkey is being pressed")
        main.Initialization()
        time.sleep(5)

    # print('not pressed')
    time.sleep(1)

