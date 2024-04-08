import fitz
import re
import nltk
from nltk.tokenize import sent_tokenize

# Assurez-vous d'avoir téléchargé les données nécessaires pour NLTK
nltk.download('punkt')

# Fonction pour détecter les éléments suspects dans le texte
def detect_suspicious_elements(text):
    suspicious_elements = []

    # Diviser le texte en phrases avec NLTK
    sentences = sent_tokenize(text, language='french')

    # Définition de motifs pour les éléments suspects
    patterns = [
        r".*?\b(très|beaucoup|étrange|inhabituel)\b.*?",
        r".*?\b(\w*?\s\w*?à la fois\b\w*?\s\w*?)\b.*?",
        r".*?\b(difficile|facile)\sà croire\b.*?"
    ]

    # Recherche des motifs dans les phrases
    for pattern in patterns:
        for sentence in sentences:
            match = re.match(pattern, sentence)
            if match:
                suspicious_elements.append(sentence.strip())

    return suspicious_elements

# Fonction pour surligner les éléments suspects dans le PDF
def highlight_suspicious_elements(pdf_path, suspicious_elements, output_path):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for element in suspicious_elements:
            instances = page.search_for(element)
            for inst in instances:
                page.add_highlight_annot(inst)

    doc.save(output_path)

# Chemin vers le document PDF
pdf_path = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\metadonnee\test_pdf\modifiedbyphotoshop\test3.pdf"

# Charger le document PDF
doc_pdf = fitz.open(pdf_path)

# Extraction du texte du PDF
text = ""
for page in doc_pdf:
    text += page.get_text()

# Détecter les éléments suspects dans le texte
suspicious_elements = detect_suspicious_elements(text)

# Surligner les éléments suspects dans le PDF
highlighted_pdf_path = "document_surligne.pdf"
highlight_suspicious_elements(pdf_path, suspicious_elements, highlighted_pdf_path)

print("Les éléments suspects ont été surlignés dans le PDF.")
