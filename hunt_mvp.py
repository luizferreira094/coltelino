import ctypes
from time import sleep
import datetime
import json
import cv2
import numpy as np
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import pytesseract
import re
import os
import uuid
import subprocess

# Define constants for the mouse events
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_F3 = 0x72
VK_ALT = 0x12
VK_1 = 0x31
VK_2 = 0x32
VK_8 = 0x38
VK_CONTROL = 0x11  # Código virtual para a tecla Ctrl
VK_V = 0x56        # Código virtual para a tecla V
VK_RETURN = 0x0D


# define the mouse_event function from ctypes
ctypes.windll.user32.mouse_event.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long]


def extract_numbers_from_image(img, scale_factor=9.0):
    # Obter as dimensões da imagem
    height, width, _ = img.shape
    
    # Definir a porcentagem da largura e altura para a ROI
    roi_percentage = 0.20  # 20% da largura e altura

    # Calcular as coordenadas da ROI centralizada
    x_start = int((width * (1 - roi_percentage)) / 2)
    x_end = int((width * (1 + roi_percentage)) / 2)
    y_start = int((height * (1 - roi_percentage)) / 2)
    y_end = int((height * (1 + roi_percentage)) / 2)

    # Cortar a região central
    roi = img[y_start:y_end, x_start:x_end]

    # Redimensionar a imagem para facilitar a detecção (aumentar o tamanho da imagem)
    new_width = int(roi.shape[1] * scale_factor)
    new_height = int(roi.shape[0] * scale_factor)
    resized_img = cv2.resize(roi, (new_width, new_height))

    # Pré-processamento da imagem para melhorar a precisão do OCR
    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    
    # Usando Thresholding binário inverso para destacar o texto branco em fundo preto
    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Aumentar o contraste da imagem para destacar ainda mais o texto
    contrast_img = cv2.convertScaleAbs(thresholded, alpha=1.5, beta=0)

    # Aplicar uma leve suavização (GaussianBlur) para reduzir o ruído
    smoothed_img = cv2.GaussianBlur(contrast_img, (3, 3), 0)

    # Usar pytesseract para extrair o texto da imagem
    custom_oem_psm_config = '--oem 1 --psm 6'  # PSM 6: Assume uma única linha de texto, OEM 1: Modelo OCR LSTM
    text = pytesseract.image_to_string(smoothed_img, config=custom_oem_psm_config)

    # Regex para capturar números no formato '58:360' (sem os colchetes)
    regex = r'\[\s*(\S+)\s*:\s*(\S+)\]'

    # Usar o regex para encontrar as correspondências
    matches = re.findall(regex, text)

    return smoothed_img, matches


def capture_active_window():
    filename='captura_janela_ativa.png'
    # Obter a janela ativa
    active_window = gw.getActiveWindow()
    
    if active_window is None:
        print("Nenhuma janela ativa encontrada!")
        return None

    # Obter as coordenadas da janela ativa
    left, top, right, bottom = active_window.left, active_window.top, active_window.right, active_window.bottom
    
    # Capturar a imagem da janela ativa
    img = ImageGrab.grab(bbox=(left, top, right, bottom))  # bbox define a área da captura
    
    # img.save(filename)

    return img

def typing_coordinates(coordinates):
     # Define the key codes for the numbers
    VK_0 = 0x30
    VK_1 = 0x31
    VK_2 = 0x32
    VK_3 = 0x33
    VK_4 = 0x34
    VK_5 = 0x35
    VK_6 = 0x36
    VK_7 = 0x37
    VK_8 = 0x38
    VK_9 = 0x39
    VK_SPACE = 0x20

    where = ' '.join(coordinates[0])
    where = where.replace("?","7")
    where = where.replace("S","5")
    sleep(2)
    # Type the input string
    for char in where:
        print(char)
        # Convert the character to the corresponding key code
        if char == '0':
            key_code = VK_0
        elif char == '1':
            key_code = VK_1
        elif char == '2':
            key_code = VK_2
        elif char == '3':
            key_code = VK_3
        elif char == '4':
            key_code = VK_4
        elif char == '5':
            key_code = VK_5
        elif char == '6':
            key_code = VK_6
        elif char == '7':
            key_code = VK_7
        elif char == '8':
            key_code = VK_8
        elif char == '9':
            key_code = VK_9
        elif char == ' ':
            key_code = VK_SPACE
        # Press the key
        ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

def generate_training_file(img_path, img_name):
    """Gera os arquivos necessários para o treinamento do Tesseract."""
    
    # Gerar o arquivo .box primeiro (Tesseract precisa dele para treinar)
    cmd_box = f"tesseract {img_path} {img_name} batch.nochop makebox"
    subprocess.run(cmd_box, shell=True)
    
    # Agora, gerar o arquivo .tr
    cmd_train = f"tesseract {img_path} {img_name} nobatch box.train"
    subprocess.run(cmd_train, shell=True)

    print(f"Arquivos .box e .tr criados para: {img_name}")

def training_model(img, status):
    """Salva a imagem na pasta correta e gera os arquivos de treinamento."""
    IMAGES_DIR = "image-training"
    SUCCESS_DIR = os.path.join(IMAGES_DIR, "success")
    FAILED_DIR = os.path.join(IMAGES_DIR, "failed")

    # Criar diretórios, se não existirem
    os.makedirs(SUCCESS_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

    # Gera um identificador único para o nome do arquivo
    unique_id = uuid.uuid4().hex
    img_filename = f"{unique_id}.tif"  # Arquivo de imagem deve ser .tif para o Tesseract
    img_path = os.path.join(SUCCESS_DIR if status == "success" else FAILED_DIR, img_filename)

    # Salva a imagem na pasta correspondente
    cv2.imwrite(img_path, img)
    print(f"Imagem salva em: {img_path}")

    # Gera o arquivo de treinamento
    generate_training_file(img_path, img_path.replace(".tif", ""))  # Passa o caminho correto

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

def teleport(warp):
    pyautogui.write(f"@warp {warp}")
    sleep(0.5)
    # Press Enter
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)
    # ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_1, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_1, 0, 2, 0)
    # ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)

def teleport_with_location(warp, coordinates):
    # ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_V, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
    # ctypes.windll.user32.keybd_event(VK_V, 0, 2, 0)

    pyautogui.write(f"@warp {warp} ")
    typing_coordinates(coordinates)
    sleep(0.5)

    # Press Enter
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)


def mobsearch(id):
    pyautogui.write(f"@mobsearch {id}")
    sleep(0.5)
    # Press Enter
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)
    sleep(1)
    # ctypes.windll.user32.keybd_event(VK_ALT, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_8, 0, 0, 0)
    # sleep(0.2)
    # ctypes.windll.user32.keybd_event(VK_8, 0, 2, 0)
    # ctypes.windll.user32.keybd_event(VK_ALT, 0, 2, 0)


def mvp_is_dead(reference_img):
    # Capturar a janela ativa
    active_window_img = capture_active_window()

    # Converter a imagem Pillow para NumPy array (OpenCV usa NumPy)
    img_np = np.array(active_window_img)

    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Converter ambas as imagens para escala de cinza
    active_window_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)

    # Realizar a correspondência (template matching)
    result = cv2.matchTemplate(active_window_gray, reference_gray, cv2.TM_CCOEFF_NORMED)

    # Encontrar o valor máximo de correspondência
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Definir um limiar para a correspondência
    threshold = 0.8  # Valor de limiar para considerar uma correspondência válida

    # Retornar True se a correspondência for maior ou igual ao limiar
    return max_val >= threshold

def use_skill():
    skill_key()
    sleep(0.1)
    left_click()

def check_coordinates():
    mobsearch(mobid)
    img = capture_active_window()
    img_array = np.array(img)
    processed_image, extraction = extract_numbers_from_image(img_array)
    # if extraction:
    #     training_model(processed_image, "success")
    # else:
    #     training_model(processed_image, "failed")
    return extraction

# set up tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# define the region of the game window to capture
game_region = (0, 0, 1440, 900)
# define the image to search for on the screen
mvp_dead = cv2.imread('mvp_dead.png')

mvps = {}
with open('mvps.json', 'r') as file:
    mvps = json.load(file)  # Carrega o conteúdo do JSON

sleep(3)
while True:    
    for warp, mobid in mvps.items():
        teleport(warp)
        sleep(1)
        # run command to check if MvP is alive
        mobsearch(mobid)
        while mvp_is_dead(mvp_dead) is False:
            location = check_coordinates()
            print(location)
            # Exibir o texto extraído (para análise)
            if location:
                location_not_changed = 1
                print(f'{mobid} esta vivo em {warp} {location}! Hora: {datetime.datetime.now()}')
                while location_not_changed:
                    teleport_with_location(warp, location)
                    sleep(0.6)
                    for i in range(0, 5):
                        use_skill()
                        sleep(2)
                    if location != check_coordinates():
                        print("MvP telou, pegando nova coordenada")
                        location_not_changed = 0
            teleport(warp)
        sleep(1)

