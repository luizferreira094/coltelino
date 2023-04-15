import ctypes
from time import sleep

# Define constants for the mouse events
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_F3 = 0x72
VK_ALT = 0x12
VK_1 = 0x31

# define the mouse_event function from ctypes
ctypes.windll.user32.mouse_event.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long]

def left_click():
    # press left mouse button down
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.1)
    # release left mouse button up
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

def skill_key():
    # Call the keyboard_event function to simulate F3
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

def teleport():
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

sleep(5)

while True:    
    skill_key()
    sleep(0.1)
    left_click()
    sleep(0.2)
    teleport()

    # validate_anti_bot

    sleep(1)