import pyautogui
import cv2
import numpy as np
import time
import ctypes
import random
from datetime import datetime
import pygetwindow as gw
import psutil

# Define the key codes for Enter
VK_F3 = 0x72
VK_F4 = 0x73
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
MOUSE_RIGHTDOWN = 0x08
MOUSE_RIGHTTUP = 0x10
VK_ALT = 0x12
VK_1 = 0x31
VK_2 = 0X32
VK_4 = 0x34
VK_5 = 0X35
VK_9 = 0x39
SCREEN_LEFT = 0
SCREEN_TOP = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

# define the image to search for on the screen
weight = cv2.imread('90_peso.png')
sell_icon = cv2.imread('sell_icon.png')
sell_list = cv2.imread('sell_list.png')
sell_list_empty = cv2.imread('sell_list_empty.png')
obb_img = cv2.imread('obb.png')
galho_seco_img = cv2.imread('galho_seco.png')
ygg_img = cv2.imread('ygg.png')
box_thunder_img = cv2.imread('box_of_thunder.png')
storage_close_button_img = cv2.imread('close_storage_button.png')

def teleport(key):
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(key, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def left_click():
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

def skill_key():
    ctypes.windll.user32.keybd_event(VK_F3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_F3, 0, 2, 0)

def get_coordinates_from_item(item):
    x, y = pyautogui.center(item)
    return int(x), int(y)

def send_storage(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.2)
    ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTTUP, 0, 0, 0, 0)
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
    if storage_button:
        x, y = get_coordinates_from_item(storage_button)
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.1)
        left_click()


def cursor_center(randomLocation=True):
    center_x = SCREEN_LEFT + SCREEN_WIDTH // 2
    center_y = SCREEN_TOP + SCREEN_HEIGHT // 2
    if randomLocation:
        random_x = random.randint(10, 50)
        random_y = random.randint(10, 50)
        ctypes.windll.user32.SetCursorPos(center_x + random_x, center_y + random_y)
    else:
        ctypes.windll.user32.SetCursorPos(center_x, center_y)

def sell():
    sell_items = pyautogui.locateOnScreen(sell_list, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    if sell_items:
        x, y = get_coordinates_from_item(sell_items)
        ctypes.windll.user32.SetCursorPos(x, y + 20)
        for i in range(100):
            ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_LEFTUP,   0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_LEFTUP,   0, 0, 0, 0)   
            time.sleep(0.1)


def sell_other_items():
    teleport(VK_5)
    time.sleep(1)
    cursor_center(randomLocation=False)
    time.sleep(0.2)
    left_click()
    time.sleep(0.3)
    sell_button = pyautogui.locateOnScreen(sell_icon, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
    if sell_button:
        x, y = get_coordinates_from_item(sell_button)
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.3)
        left_click()
        time.sleep(0.3)
        sell()
        sell_button = pyautogui.locateOnScreen(sell_icon, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        if sell_button:
            x, y = get_coordinates_from_item(sell_button)
            ctypes.windll.user32.SetCursorPos(x, y)
            time.sleep(0.3)
            left_click()
            time.sleep(0.3)
            cursor_center(randomLocation=False)
            print(f"venda realizada!  Hora: {datetime.now()}")

def send_items_to_storage(items):
    for item in items:
        item_pixel = pyautogui.locateOnScreen(item, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
        # time.sleep(0.3)
        if item_pixel:
            item_location_x, item_location_y = get_coordinates_from_item(item_pixel)
            open_storage()
            time.sleep(0.1)
            send_storage(item_location_x, item_location_y)
            time.sleep(0.1)
            close_storage()
            teleport(VK_9)

def cpu_usage_high(threshold=70):
    return psutil.cpu_percent(interval=1) > threshold

farmed_items = [ygg_img, galho_seco_img, box_thunder_img, obb_img]

time.sleep(5)
print("Iniciando bot...")

try:
    active_window = gw.getActiveWindow()
    if active_window:
        SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT = active_window.left, active_window.top, active_window.width, active_window.height
        while True:
            try:
                if cpu_usage_high():
                    print("Uso de CPU alto, aguardando baixar...")
                    while cpu_usage_high():
                        time.sleep(1)

                weight_heavy = pyautogui.locateOnScreen(weight, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8)
                if weight_heavy is not None:
                    send_items_to_storage(farmed_items)
                    # sell_other_items()
                cursor_center()
                skill_key()
                left_click()
                teleport(VK_1)
                time.sleep(0.5)
            except Exception as e:
                print(f"[ERRO NO LOOP] {e}")
                time.sleep(1)
    else:
        print("Nenhuma janela ativa encontrada.")

except KeyboardInterrupt:
    print("Bot interrompido manualmente.")

finally:
    print("Encerrando com segurança.")
