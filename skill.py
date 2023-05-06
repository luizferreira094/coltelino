import ctypes
from time import sleep



VK_F3 = 0x72


def press_skill():
        # Press the key
        ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

def wait(seconds):
        sleep(seconds)

wait(3)
while True:
    press_skill()
    wait(0.1)