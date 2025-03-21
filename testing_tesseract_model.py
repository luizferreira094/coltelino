import pytesseract
from PIL import Image
import os

# Carregar imagem .tif
image = Image.open("image-training/failed/b92e71dbd7f949ba94490e813785ab69.tif")
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files (x86)\Tesseract-OCR\tessdata"

# Extrair texto usando o modelo treinado
text = pytesseract.image_to_string(image, config="--oem 1 --psm 6 -c tessedit_char_whitelist=\"0123456789:., []\"")

print(text)
