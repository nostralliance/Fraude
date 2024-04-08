import fitz  # PyMuPDF

def detecter_fraude_documentaire(pdf_path):
    """
    Fonction pour détecter la fraude documentaire dans un fichier PDF.
    """
    # Ouvrir le fichier PDF
    document = fitz.open(pdf_path)

    # Extraire les métadonnées
    metadata = document.metadata

    # Vérifier la présence de métadonnées suspects
    for key, value in metadata.items():
        if isinstance(value, bytes):
            value = value.decode("utf-8", "ignore")
        print(f"{key}: {value}")

    # Analyser les modifications de texte sur chaque page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        page_text = page.get_text()
        original_text = page_text
        # Exemple : Vérifier si le texte a été modifié
        if len(original_text) != len(page_text):
            print(f"Alerte : Modification de texte détectée sur la page {page_num + 1}")

    # Fermer le document
    document.close()

# Exemple d'utilisation
pdf_path = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\metadonnee\test_pdf\sharp\14sharp.pdf"
detecter_fraude_documentaire(pdf_path)