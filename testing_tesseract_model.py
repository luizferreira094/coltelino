import pytesseract
from PIL import Image
import os

# Carregar imagem .tif
image = Image.open("image-training/success/28073d390c304306a419163289f385a7.tif")

# os.environ["TESSDATA_PREFIX"] = r"C:\Program Files (x86)\Tesseract-OCR\tessdata"

# Extrair texto usando o modelo treinado
text = pytesseract.image_to_string(image, config="--oem 1 --psm 6 -l ragnarok_coordinates -c tessedit_char_whitelist=\"0123456789:., []\"")

print(text)
