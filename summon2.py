import pyautogui
import cv2
import time
import ctypes


# Define the key codes for Enter
VK_F3 = 0x72
VK_F5 = 0x74
VK_F6 = 0x75
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_ALT = 0x12
VK_1 = 0x31

# define the region of the game window to capture
# game_region = (0, 0, 1360, 768)

# define the image to search for on the screen
popup_skill = cv2.imread('summon.png')

# define the casting image to search for on the screen
popup_cast = cv2.imread('cast.png')

# define the dilema image to search on the screen
poput_dilema = cv2.imread('dilema.png')


def break_branch():
    ctypes.windll.user32.keybd_event(VK_F6, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F6, 0, 2, 0)

def click():
    # press left mouse button down
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    # release left mouse button up
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

def teleport():
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)


# define the wait variable for waiting press button
wait = False

time.sleep(5)

while True:
    # take a screenshot of the game window
    # game_screenshot = pyautogui.screenshot(region=game_region)
    game_screenshot = pyautogui.screenshot()

    # search for the popup window on the screenshot
    summon_skill = pyautogui.locateOnScreen(popup_skill, confidence=0.5)
    casting = pyautogui.locateOnScreen(popup_cast, confidence=0.5)
    dilema = pyautogui.locateOnScreen(poput_dilema, confidence=0.7)

    if summon_skill is not None:
        print("Summon Time! Good Luck!")
        break_branch()
        time.sleep(1)
        click()
        # wait = True
        # while (wait):
        #     time.sleep(0.1)
        #     if pyautogui.locateOnScreen(popup_skill, confidence=0.5) is None:
        #         wait = False
    
    if casting is not None:
        print("canceling skill")
        ctypes.windll.user32.keybd_event(VK_F5, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F5, 0, 2, 0)

    if dilema is not None:
        time.sleep(0.1)
        print("teleporting!")
        teleport()

    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

    # wait for 1 second before taking the next screenshot
    time.sleep(0.1)