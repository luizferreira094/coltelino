import pyautogui
import cv2
import numpy as np
import time
import ctypes
import random
from datetime import datetime
import pygetwindow as gw


# Define the key codes for Enter
VK_F3 = 0x72
VK_F4 = 0x73
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
MOUSE_RIGHTDOWN = 0x08
MOUSE_RIGHTTUP = 0x10
VK_ALT = 0x12
VK_1 = 0x31
VK_4 = 0x34
VK_5 = 0X35

SCREEN_LEFT = 0
SCREEN_TOP = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

# define the region of the game window to capture
# game_region = (0, 0, 1360, 768)

# define the image to search for on the screen
weight = cv2.imread('90_peso.png')

# define the image to search for on the screen
sell_icon = cv2.imread('sell_icon.png')

# define the image to search for on the screen
sell_list = cv2.imread('sell_list.png')

# define the image to search for on the screen
sell_list_empty = cv2.imread('sell_list_empty.png')

# # define the image to search for on the screen
# obb_img = cv2.imread('obb.png')

# # define the image to search for on the screen
# galho_seco_img = cv2.imread('galho_seco.png')

# define the image to search for on the screen
ygg_img = cv2.imread('ygg.png')


storage_close_button_img = cv2.imread('close_storage_button.png')
# # define the image to search for on the screen
# coma_img = cv2.imread('coma.png')


def teleport(key):
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(key, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def left_click():
    # press left mouse button down
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    # release left mouse button up
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

def skill_key():
    # Call the keyboard_event function to simulate F3
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

def get_coordinates_from_item(item):
    x, y = pyautogui.center(item)
    x, y = int(x), int(y)
    return x, y

def send_storage(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(1)
    # click ctrl
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.3)
    # press right mouse button down
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    # release right mouse button up
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTTUP, 0, 0, 0, 0)
    # release ctrl
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def open_storage():
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_4, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_4, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)    

def close_storage():
    storage_button = pyautogui.locateOnScreen(storage_close_button_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    x, y = get_coordinates_from_item(storage_button)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.3)
    left_click()

def cursor_center(randomLocation=True):
    # Calcula o centro da janela
    center_x = SCREEN_LEFT + SCREEN_WIDTH // 2
    center_y = SCREEN_TOP + SCREEN_HEIGHT // 2

    if randomLocation:
        random_x = random.randint(10, 50)
        random_y = random.randint(10, 50)
        # Move o mouse de volta para o centro da tela
        ctypes.windll.user32.SetCursorPos(center_x+random_x, center_y+random_y)
    else:
        ctypes.windll.user32.SetCursorPos(center_x, center_y)


def sell():
    sell_items = pyautogui.locateOnScreen(sell_list, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    x, y = get_coordinates_from_item(sell_items)
    ctypes.windll.user32.SetCursorPos(x, y+20)
     # Call the keyboard_event function to simulate F4
    ctypes.windll.user32.keybd_event(VK_F4, 0, 0, 0)
    time.sleep(6)
    ctypes.windll.user32.keybd_event(VK_F4, 0, 2, 0)

def sell_other_items():
    teleport(VK_5)
    time.sleep(1)
    left_click()
    time.sleep(0.3)
    sell_button = pyautogui.locateOnScreen(sell_icon, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    x, y = get_coordinates_from_item(sell_button)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.3)
    left_click()
    time.sleep(0.3)
    sell()

    sell_button = pyautogui.locateOnScreen(sell_icon, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    x, y = get_coordinates_from_item(sell_button)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.3)
    left_click()
    time.sleep(0.3)
    cursor_center(randomLocation=False)
    print(f"venda realizada!  Hora: {datetime.now()}")



time.sleep(5)


active_window = gw.getActiveWindow()
# Verifica se a janela ativa foi encontrada
if active_window:
    # Obtém as coordenadas (x, y) e o tamanho (largura, altura) da janela ativa
    SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT = active_window.left, active_window.top, active_window.width, active_window.height

    while True:
        # search for the popup window on the screenshot
        weight_heavy = pyautogui.locateOnScreen(weight, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.97)

        if weight_heavy is not None:
            # obb_item = pyautogui.locateOnScreen(obb_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
            # gs_item = pyautogui.locateOnScreen(galho_seco_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.5)
            ygg_item = pyautogui.locateOnScreen(ygg_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.6)

            open_storage()
            
            # if obb_item:
            #     obb_location_x, obb_location_y = get_coordinates_from_item(obb_item)
            #     send_storage(obb_location_x, obb_location_y)
            # if gs_item:
            #     gs_location_x, gs_location_y = get_coordinates_from_item(gs_item)
            #     send_storage(gs_location_x, gs_location_y)
            if ygg_item:
                ygg_location_x, ygg_location_y = get_coordinates_from_item(ygg_item)
                send_storage(ygg_location_x, ygg_location_y)
            time.sleep(0.3)
            close_storage()
            time.sleep(0.2)
            cursor_center(randomLocation=False)
            time.sleep(0.4)
            sell_other_items()
        
        cursor_center()
        skill_key()
        left_click()
        teleport(VK_1)
        time.sleep(2)

else:
    print("Nenhuma janela ativa encontrada.")    

