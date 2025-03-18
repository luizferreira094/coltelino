import pyautogui
import cv2
import numpy as np
import time
import ctypes


# Define the key codes for Enter
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F5 = 0x74
VK_DOWN = 0x28
VK_RETURN = 0x0D
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_ALT = 0x12
VK_1 = 0x31

# define the region of the game window to capture
# game_region = (0, 0, 1360, 768)

# define the image to search for on the screen
popup_skill = cv2.imread('summon.png')

# define the image to search for on the screen
popup_cast = cv2.imread('cast.png')

# define the image to search for on the screen
popup_portal = cv2.imread('portal_popup.png')

# define the image to search for on the screen
dead_screen = cv2.imread('dead.png')

# define the image to search for on the screen
dead_button = cv2.imread('dead_OK.png')

# define the image to search for on the screen
dillema_screen = cv2.imread('dillema.png')

# define the image to search for on the screen
esconderijo_flag = cv2.imread('esconderijo.png')

# # define the image to search for on the screen
# coma_img = cv2.imread('coma.png')


def teleport():
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def cursor_center():
    # Obtém o tamanho da tela
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    # Move o mouse de volta para o centro da tela
    ctypes.windll.user32.SetCursorPos(center_x, center_y)
    print("Mouse voltou ao centro da tela!")

# define the wait variable for waiting press button
wait = False

time.sleep(5)

while True:
    # take a screenshot of the game window
    # game_screenshot = pyautogui.screenshot(region=game_region)
    game_screenshot = pyautogui.screenshot()

    # search for the popup window on the screenshot
    summon_skill = pyautogui.locateOnScreen(popup_skill, confidence=0.5)
    cast_skill = pyautogui.locateOnScreen(popup_cast, confidence=0.5)
    portal_skill = pyautogui.locateOnScreen(popup_portal, confidence=0.5)
    dead_popup = pyautogui.locateOnScreen(dead_screen, confidence=0.8)
    dillema_skill = pyautogui.locateOnScreen(dillema_screen, confidence=0.8)
    esconderijo_skill = pyautogui.locateOnScreen(esconderijo_flag, confidence=0.8)
    # coma_skill = pyautogui.locateOnScreen(coma_img, confidence=0.8)

    if summon_skill is not None:
        print("Summon Time! Good Luck!")
        # Press F2
        ctypes.windll.user32.keybd_event(VK_F2, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F2, 0, 2, 0) 
        time.sleep(0.5)
        # press left mouse button down
        ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        # release left mouse button up
        ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

        teleport()
        # MANUAL SUMMONING - NOT ERASE
        # wait = True
        # while (wait):
        #     time.sleep(0.1)
        #     if pyautogui.locateOnScreen(popup_skill, confidence=0.5) is None:
        #         wait = False

    if portal_skill is not None:
        print("Canceling portal popup")
        # Press down arrow 2x
        ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)      

        ctypes.windll.user32.keybd_event(VK_DOWN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_DOWN, 0, 2, 0)      
        time.sleep(0.5)
        # Press Enter
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)    

    if dead_popup is not None:
        x, y = pyautogui.center(dead_popup)
        x, y = int(x), int(y)
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.2)
        # press left mouse button down
        ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        # release left mouse button up
        ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.5)
        ok_button = pyautogui.locateOnScreen(dead_button, confidence=0.8)
        time.sleep(0.5)
        if ok_button:
            x, y = pyautogui.center(ok_button)
            x, y = int(x), int(y)
            ctypes.windll.user32.SetCursorPos(x, y)
            time.sleep(0.1)
            # press left mouse button down
            ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            # release left mouse button up
            ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)
            
        time.sleep(2)
        cursor_center()
        teleport()

    if cast_skill is not None:
        print("canceling skill")
        # Press Enter
        ctypes.windll.user32.keybd_event(VK_F5, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F5, 0, 2, 0)

    if dillema_skill is not None:
        teleport()

    if esconderijo_skill is not None:
        teleport()

    # Press Enter
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

    # wait for 1 second before taking the next screenshot
    time.sleep(0.1)