import easyocr
import cv2
import re

def detect_date_in_image(image_path):
    # Créer un objet EasyOCR en français
    reader = easyocr.Reader(['fr'])
    
    # Charger l'image
    image = cv2.imread(image_path)
    
    # Utiliser EasyOCR pour lire l'image
    results = reader.readtext(image)
    
    # Parcourir les résultats pour chercher une date
    for (bbox, text, prob) in results:
        if is_date(text):
            return text
    
    # Aucune date n'a été trouvée
    return False

def is_date(text):
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
    if re.match(date_pattern, text):
        return True
    return False

# Chemin de l'image que vous souhaitez analyser
image_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\OCR\essaie_1.png'

# Appeler la fonction pour détecter une date
date_found = detect_date_in_image(image_path)

# Si une date est trouvée, date_found sera True, sinon ce sera False
print(date_found)
