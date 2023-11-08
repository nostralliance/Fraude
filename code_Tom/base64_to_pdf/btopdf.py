from base64 import b64decode
from mylib import paths, functions, criterias, constants
from typing import Tuple
import fitz, os
from PIL import Image
import json


result = []
entree = input('choisissez le type d entree du fichier :')

if entree == 'base64':

    pdf_data = functions.base64topdf()

    with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\output.pdf', 'wb') as pdf_out:
        pdf_out.write(pdf_data)

    pdfFile = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\output.pdf'
    pages = None  # traiter toutes les pages
    png_files = functions.pdf2img(pdfFile, pages)

    for pngFile in png_files:
        print("---Traitement de la page : " + os.path.basename(pngFile) + "...")
        # On récuprère le texte extrait du png
        pngText = functions.img2text(pngFile)
        result_ocr = criterias.dateferiee(pngText)
        if result_ocr == True:
            result.append(result_ocr)
            break

elif entree == 'pdf':
    pdfFile = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\essaie_facture\ferie2.pdf'
    pages = None  # traiter toutes les pages
    png_files = functions.pdf2img(pdfFile, pages)

    for pngFile in png_files:
        print("---Traitement de la page : " + os.path.basename(pngFile) + "...")
        # On récuprère le texte extrait du png
        pngText = functions.img2text(pngFile)
        result_ocr = criterias.dateferiee(pngText)
        if result_ocr == True:
            result.append(result_ocr)
            break

elif entree == 'image':
    print('entree image')



result_dict = {
    "date_feriee_trouvee": bool(result),  # True si une date a été trouvée, False sinon
}

with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\result.json', 'w') as json_file:
    json.dump(result_dict, json_file)

