import pyautogui
import cv2
import numpy as np
import time
import ctypes
import pygetwindow as gw


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

SCREEN_LEFT = 0
SCREEN_TOP = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

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

# define the image to search for on the screen
invocar_monstro_img = cv2.imread('invocar_monstro.png')

# define the image to search for on the screen
id_item_list_img = cv2.imread('id_item_list.png')
# # define the image to search for on the screen
# coma_img = cv2.imread('coma.png')


def teleport():
    global use_dead_branch
    use_dead_branch = True
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_1, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def cursor_center():
    # Calcula o centro da janela
    center_x = SCREEN_LEFT + SCREEN_WIDTH // 2
    center_y = SCREEN_TOP + SCREEN_HEIGHT // 2

    ctypes.windll.user32.SetCursorPos(center_x, center_y)
    print("Mouse voltou ao centro da tela!")

# define the wait variable for waiting press button
wait = False
use_dead_branch = True

time.sleep(5)


active_window = gw.getActiveWindow()
# Verifica se a janela ativa foi encontrada

if active_window:
    # Obtém as coordenadas (x, y) e o tamanho (largura, altura) da janela ativa
    SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT = active_window.left, active_window.top, active_window.width, active_window.height

    while True:
        # search for the popup window on the screenshot
        summon_skill = pyautogui.locateOnScreen(popup_skill, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
        cast_skill = pyautogui.locateOnScreen(popup_cast, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
        portal_skill = pyautogui.locateOnScreen(popup_portal, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
        dead_popup = pyautogui.locateOnScreen(dead_screen, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        dillema_skill = pyautogui.locateOnScreen(dillema_screen, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        esconderijo_skill = pyautogui.locateOnScreen(esconderijo_flag, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        invocar_monstro_skill = pyautogui.locateOnScreen(invocar_monstro_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
        id_item_list_popup = pyautogui.locateOnScreen(id_item_list_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        # coma_skill = pyautogui.locateOnScreen(coma_img, confidence=0.8)

        if summon_skill is not None:
            print("Summon Time! Good Luck!")
            # Press F2

            if use_dead_branch:
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

        if invocar_monstro_skill is not None:
            print("invocado monstro pela skill")
            use_dead_branch = False

        if id_item_list_popup is not None:
            teleport()

        # Press Enter
        ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

        # wait for 1 second before taking the next screenshot
        time.sleep(0.1)
else:
    print("Nenhuma janela ativa encontrada.")    


