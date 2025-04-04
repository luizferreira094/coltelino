import ctypes
from time import sleep
import cv2
import numpy as np
import pyautogui
import pytesseract

# Define constants for the mouse events
MOUSE_LEFTDOWN = 0x02
MOUSE_LEFTUP = 0x04
VK_F3 = 0x72
VK_ALT = 0x12
VK_1 = 0x31
VK_RETURN = 0x0D

# define the mouse_event function from ctypes
ctypes.windll.user32.mouse_event.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long]

def extract_red_colours(image):
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the red color
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours of the red regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours and extract the bounding boxes
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

def extract_ocr(image):
    return pytesseract.image_to_string(image)

def game_event(code):
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

    code = code.replace("S","5")
    code = code.replace("?","7")
    code_string = ''.join(filter(str.isdigit, code))
    print("start typing code: [%s]" % code_string)
    sleep(2)

    # Type the input string
    for char in code_string:
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
        # Press the key
        ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)
    print("done typing")
    sleep(2)
    # Press Enter
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)

    # # Press Enter
    # ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    # ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)

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


# set up tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# define the region of the game window to capture
game_region = (0, 0, 1360, 768)

# define the region of the popup window to capture
#popup_region = (300, 200, 500, 300)
popup_region = (0, 0, 1360, 768)

# define the image to search for on the screen
popup_image = cv2.imread('BotInput.JPG')

sleep(3)
while True:    
    # take a screenshot of the game window
    game_screenshot = pyautogui.screenshot(region=game_region)

    # search for the popup window on the screenshot
    popup_location = pyautogui.locateOnScreen(popup_image, confidence=0.5)

    if popup_location is not None:

        print("Press enter after anti-bot initialized")

        # Press Enter
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)

        sleep(1)

        # take a screenshot of the popup window
        popup_screenshot = pyautogui.screenshot(region=popup_location)

        # convert the screenshot to a numpy array
        popup_np = np.array(popup_screenshot)

        # red_extracted = extract_red_colours(popup_np)

        cv2.imwrite('processed_image.jpg', popup_np)

        # gray = cv2.cvtColor(popup_np, cv2.COLOR_BGR2GRAY)

        lower_red = np.array([60, 0, 0])
        upper_red = np.array([255, 0, 0])

        # Threshold the image to extract the red color
        red = cv2.inRange(popup_np, lower_red, upper_red)

        resize = cv2.resize(red, None, fx=15, fy=15, interpolation=cv2.INTER_CUBIC)

        cv2.imwrite('processed_image_number.jpg', resize)

        red_text = extract_ocr(resize)

        # Print the extracted text
        print(red_text)

        game_event(red_text)

    skill_key()
    sleep(0.1)
    left_click()
    sleep(0.2)
    teleport()

    sleep(1.7)