import pyautogui
import cv2
import numpy as np
import time
import ctypes


# Define the key codes for Enter
VK_F3 = 0x72

# define the region of the game window to capture
game_region = (0, 0, 1360, 768)

# define the region of the popup window to capture
#popup_region = (300, 200, 500, 300)
popup_region = (0, 0, 1360, 768)

# define the image to search for on the screen
popup_image = cv2.imread('summon.png')

time.sleep(5)

while True:
    # take a screenshot of the game window
    game_screenshot = pyautogui.screenshot(region=game_region)


    # convert the screenshot to a numpy array
    popup_np = np.array(game_screenshot)

    # red_extracted = extract_red_colours(popup_np)

    cv2.imwrite('summon_screen.jpg', popup_np)

    # search for the popup window on the screenshot
    popup_location = pyautogui.locateOnScreen(popup_image)

    if popup_location is not None:
        print("Summon Time! Good Luck!")
        time.sleep(10)
    
    # Press Enter
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

    # wait for 1 second before taking the next screenshot
    time.sleep(1)