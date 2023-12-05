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
        text_list.extend(page.get_text("text").splitlines())  # Divisez le texte en lignes
    pdf_document.close()
    return text_list

def extract_words_from_image(image_path, reader):
    image = Image.open(image_path)
    text_results = reader.readtext(np.array(image))
    words = [word_info[1] for word_info in text_results]
    return words

# Chemin du fichier PDF
pdf_path = r"C:\Users\tomlo\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\Facture N°2 - Jean.pdf"

# Extraire les lignes du PDF
pdf_line_list = extract_text_from_pdf(pdf_path)

# Utiliser EasyOCR pour extraire du texte à partir d'une image
image_path = r"C:\Users\tomlo\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\Facture N°2 - Jean_page-0001.jpg"  # Remplacez cela par le chemin de votre image
reader = easyocr.Reader(['fr'])  # Spécifiez les langues que vous souhaitez prendre en charge
image_word_list = extract_words_from_image(image_path, reader)

matched_lines_and_words = {}

for pdf_line in pdf_line_list:
    match_found = False
    for image_word in image_word_list:
        closest_match = get_close_matches(image_word, [pdf_line], n=1, cutoff=0.7)
        if closest_match:
            matched_lines_and_words[pdf_line] = closest_match[0]
            match_found = True
            break  # Sortir de la boucle interne dès qu'une correspondance est trouvée
    if not match_found:
        matched_lines_and_words[pdf_line] = None  # Aucune correspondance trouvée

# Afficher les correspondances trouvées
for pdf_line, matched_word in matched_lines_and_words.items():
    if matched_word is None:
        print(f"PDF Line: {pdf_line} | No Match Found")
    else:
        print(f"PDF Line: {pdf_line} | Matched Word: {matched_word}")
