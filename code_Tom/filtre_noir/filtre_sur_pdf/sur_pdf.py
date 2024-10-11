import fitz  # PyMuPDF

def invert_pdf_colors(pdf_path, output_path):
    # Ouvrir le document PDF
    pdf_document = fitz.open(pdf_path)

    # Itérer à travers chaque page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Obtenir le contenu de la page
        text_instances = page.get_text("dict")
        
        # Inverser les couleurs du texte
        for block in text_instances["blocks"]:
            if block["type"] == 0:  # Vérifier que le bloc est du texte
                for line in block["lines"]:
                    for span in line["spans"]:
                        span_color = span["color"]
                        if isinstance(span_color, list):
                            span["color"] = [1 - float(c) for c in span_color]

        # Obtenir les objets de dessin de la page
        for obj in page.get_drawings():
            if obj['type'] in ['line', 'rect', 'curve']:
                color = obj['color']
                if isinstance(color, list):
                    obj['color'] = [1 - float(c) for c in color]

        # Sauvegarder les modifications sur la page
        # Note: This part may need to be adjusted depending on the library capabilities
        # The exact method to set updated text and drawing objects might differ.
        # page.set_text(text_instances) - this function may not exist or may need a different approach

    # Sauvegarder le PDF modifié
    pdf_document.save(output_path)
    pdf_document.close()

# Exemple d'utilisation
invert_pdf_colors(r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\filtre_noir\base\FACTURE A CONTROLER.pdf', r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\filtre_noir\res\FACTURE_A_CONTROLER_INVERTED.pdf')
