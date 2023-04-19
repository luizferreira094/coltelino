import pyautogui
import cv2
import numpy as np
import time
import ctypes


# Define the key codes for Enter
VK_F3 = 0x72
VK_F5 = 0x74

# define the region of the game window to capture
game_region = (0, 0, 1360, 768)

# define the image to search for on the screen
popup_skill = cv2.imread('summon.png')

# define the image to search for on the screen
popup_cast = cv2.imread('cast.png')

time.sleep(5)

while True:
    # take a screenshot of the game window
    game_screenshot = pyautogui.screenshot(region=game_region)

    # search for the popup window on the screenshot
    summon_skill = pyautogui.locateOnScreen(popup_skill, confidence=0.5)
    cast_skill = pyautogui.locateOnScreen(popup_cast, confidence=0.5)

    if summon_skill is not None:
        print("Summon Time! Good Luck!")
        time.sleep(5)
    
    if cast_skill is not None:
        print("canceling skill")
        # Press Enter
        ctypes.windll.user32.keybd_event(VK_F5, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F5, 0, 2, 0)

    # Press Enter
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

    # wait for 1 second before taking the next screenshot
    time.sleep(0.2)