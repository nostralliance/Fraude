import easyocr
import fitz
from PIL import Image
import numpy as np
from difflib import get_close_matches

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_list = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text_list.extend(page.get_text("text").split())  # Divisez le texte en mots
    pdf_document.close()
    return text_list

def extract_lines_from_image(image_path, reader):
    image = Image.open(image_path)
    text_results = reader.readtext(np.array(image))
    lines = [result[1] for result in text_results]
    return lines

# Chemin du fichier PDF
pdf_path = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\Facture N°2 - Jean.pdf"

# Extraire les mots du PDF
pdf_word_list = extract_text_from_pdf(pdf_path)

# Utiliser EasyOCR pour extraire du texte à partir d'une image
image_path = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\Facture N°2 - Jean_page-0001.jpg"  # Remplacez cela par le chemin de votre image
reader = easyocr.Reader(['fr'])  # Spécifiez les langues que vous souhaitez prendre en charge
image_line_list = extract_lines_from_image(image_path, reader)

# Correspondance souple entre les mots du PDF et les mots de l'image
matched_words = {}

for pdf_word in pdf_word_list:
    closest_matches = get_close_matches(pdf_word, image_line_list, n=1, cutoff=0.7)
    if closest_matches:
        matched_words[pdf_word] = closest_matches[0]

# Afficher les correspondances trouvées
for pdf_word, image_word in matched_words.items():
    print(f"PDF Word: {pdf_word} | Image Word: {image_word}")
