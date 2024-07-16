import cv2
import pytesseract
from PIL import Image
import os
import time

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para resaltar el texto
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Guardar la imagen procesada (opcional)
    processed_image_path = "processed_image.png"
    cv2.imwrite(processed_image_path, binary)

    return processed_image_path


def extract_text_from_image(image_path):
    # Preprocesar la imagen
    processed_image_path = preprocess_image(image_path)

    # Usar Tesseract para extraer texto
    extracted_text = pytesseract.image_to_string(Image.open(processed_image_path), lang='es')
    
    return extracted_text

def extract_player_info(image_path):
    extracted_text = extract_text_from_image(image_path)
    time.sleep(1)
    print(extracted_text)

    # Parsear el texto extraído para obtener la información relevante
    # lines = extracted_text.split('\n')
    # player_info = {
    #     "Nombre": lines[0] if len(lines) > 0 else "Desconocido",
    #     "Alianza": lines[2] if len(lines) > 2 else "Desconocido",
    #     "Poder": lines[4] if len(lines) > 4 else "Desconocido",
    #     "Méritos": lines[5] if len(lines) > 5 else "Desconocido",
    #     "ID": lines[3] if len(lines) > 3 else "Desconocido"
    # }

    return player_info

# Ejemplo de uso
image_path = "mtg.png"
player_info = extract_player_info(image_path)
print(player_info)
