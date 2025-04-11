import ctypes
import json
import cv2
import numpy as np
import pytesseract
import os
import uuid
import subprocess
from time import sleep
from datetime import datetime
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import re

# Constantes
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_RETURN = 0x0D
VK_TAB = 0x09
VK_F3 = 0x72
VK_CONTROL = 0x11
VK_V = 0x56
KEY_CODES = {str(i): 0x30 + i for i in range(10)}
KEY_CODES.update({' ': 0x20})

SCREEN_LEFT = 0
SCREEN_TOP = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

def press_key(key_code, hold_time=0.1):
    """Simula o pressionamento de uma tecla."""
    ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
    sleep(hold_time)
    ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

def click_left():
    """Simula um clique esquerdo do mouse."""
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.1)
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, 0, 0, 0, 0)

def capture_active_window():
    """Captura a tela da janela ativa."""
    active_window = gw.getActiveWindow()
    if not active_window:
        print("Nenhuma janela ativa encontrada!")
        return None
    return ImageGrab.grab(bbox=(active_window.left, active_window.top, active_window.right, active_window.bottom))

def extract_numbers_from_image(img, scale_factor=9.0):
    """Extrai números da imagem usando OCR."""
    height, width, _ = img.shape
    roi = img[int(height*0.4):int(height*0.6), int(width*0.4):int(width*0.6)]
    resized_img = cv2.resize(roi, None, fx=scale_factor, fy=scale_factor)
    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    smoothed_img = cv2.GaussianBlur(cv2.convertScaleAbs(thresholded, alpha=1.5, beta=0), (3, 3), 0)
    text = pytesseract.image_to_string(smoothed_img, config='--oem 1 --psm 6 -c tessedit_char_whitelist=\"0123456789:., []\"')
    print("extracted text: "+text)
    return smoothed_img, re.findall(r'\[\s*(\S+)\s*:\s*(\S+)\]', text)

def type_coordinates(coordinates):
    """Digita as coordenadas corrigindo possíveis erros de OCR."""
    where = ' '.join(coordinates[0]).replace("?", "7").replace("S", "5").replace("W", "77")
    for char in where:
        if char in KEY_CODES:
            press_key(KEY_CODES[char])

def generate_training_file(img_path, img_name):
    """Gera arquivos de treinamento para o Tesseract."""
    subprocess.run(f"tesseract {img_path} {img_name} batch.nochop makebox", shell=True)
    subprocess.run(f"tesseract {img_path} {img_name} nobatch box.train", shell=True)

def save_training_image(img):
    """Salva a imagem na pasta correspondente e gera arquivos de treinamento."""
    base_dir = os.path.join("image-training", "curated_files")
    os.makedirs(base_dir, exist_ok=True)
    img_path = os.path.join(base_dir, f"{uuid.uuid4().hex}.tif")
    cv2.imwrite(img_path, img)
    generate_training_file(img_path, img_path.replace(".tif", ""))

def teleport(warp, coordinates=None):
    """Teleporta para um warp opcionalmente com coordenadas."""
    if coordinates:
        pyautogui.write(f"@warp {warp} ")
        type_coordinates(coordinates)
    else:
        pyautogui.write(f"@warp {warp}")
    sleep(0.5)
    press_key(VK_RETURN)

def check_coordinates(mobid):
    """Busca um mob e extrai suas coordenadas."""
    pyautogui.write(f"@mobsearch {mobid}")
    press_key(VK_RETURN)
    sleep(0.5)
    img = capture_active_window()
    if img:
        processed_image, extraction = extract_numbers_from_image(np.array(img))
        print(extraction)
        # save_training_image(processed_image)
        return extraction

def nearby(location):
    """Verifica se a localização do mob mudou."""
    new_location = check_coordinates()
    return any(abs(int(t1) - int(t2)) <= 10 for t1, t2 in zip(location, new_location)) if new_location else False

def mvp_is_dead(reference_img):
    if pyautogui.locateOnScreen(reference_img, region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT), confidence=0.8) is not None:
        return True 
    else:
        return False


"""Loop principal do script."""
with open('mvps.json', 'r') as file:
    mvps = json.load(file)
mvp_dead_img = cv2.imread('mvp_dead.png')
mvp_dead_img2 = cv2.imread('mvp_dead2.png')
sleep(3)
active_window = gw.getActiveWindow()
if active_window:
    # Obtém as coordenadas (x, y) e o tamanho (largura, altura) da janela ativa
    SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT = active_window.left, active_window.top, active_window.width, active_window.height
    while True:
        for warp, mobids in mvps.items():
            for mobid in mobids:
                teleport(warp)
                sleep(1)
                pyautogui.write(f"@mobsearch {mobid}")
                press_key(VK_RETURN)
                sleep(0.5)
                while not (mvp_is_dead(mvp_dead_img) or mvp_is_dead(mvp_dead_img2)):
                    location = check_coordinates(mobid)
                    print(location)
                    if location:
                        print(f'{mobid} está vivo em {warp} {location}! Hora: {datetime.now()}')
                        teleport(warp, location)
                        sleep(0.6)
                        press_key(VK_F3, 10)
                        sleep(1)
                        press_key(VK_RETURN)
                        press_key(VK_RETURN)
                    teleport(warp)
                    sleep(0.3)
                    pyautogui.write(f"@mobsearch {mobid}")
                    press_key(VK_RETURN)
                    sleep(1)
else:
    print("Nenhuma janela ativa encontrada.")    
  

