from flask import Flask, jsonify
import os
import easyocr
import re
from PIL import Image
import numpy as np

app = Flask(__name__)
image_folder = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\OCR"

reader = easyocr.Reader(['fr'])

def scan_images_for_dates():
    for parent, dnames, fnames in os.walk(image_folder):
        for fname in fnames:
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(image_folder, fname)
                text = extract_text_from_image(image_path)
                if contains_date(text):
                    return True
    return False

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    img_np = np.array(img)  # Convertir l'image PIL en tableau NumPy
    result = reader.readtext(img_np)
    text = " ".join([entry[1] for entry in result])
    print(text)
    return text

def contains_date(text):
    date_pattern = r"\b\d{1,2}/\d{1,2}/\d{4}\b"
    return bool(re.search(date_pattern, text))

@app.route('/check_for_dates', methods=['GET'])
def check_for_dates():
    if scan_images_for_dates():
        return jsonify({'dates_found': True})
    return jsonify({'dates_found': False})

if __name__ == '__main__':
    app.run(debug=True)
