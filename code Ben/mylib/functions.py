import fitz, os
import easyocr
from typing import Tuple
from . import paths


# On instancie l'extracteur OCR
reader = easyocr.Reader(['en','fr'], gpu=False)

def pdf2img(society: str, pdfFile: str ,pages: Tuple = None):
    # On charge le document
    pdf = fitz.open(pdfFile)
    # On détermine la liste des fichiers générés
    pngFiles = []
    # Pour chaque page du pdf
    for pageId in range(pdf.pageCount):

        if str(pages) != str(None):
            if str(pageId) not in str(pages):
                continue

        # On récupère la page courante
        page = pdf[pageId]
        # On convertit la page courante
        pageMatrix = fitz.Matrix(2, 2).preRotate(int(0))
        pagePix = page.getPixmap(matrix=pageMatrix, alpha=False)
        # On exporte la page générée
        pngPath = str(paths.rootPath) + '/' + society + '/' + paths.tmpDir + os.path.basename(pdfFile) +'/'
        # Si le répertoire dédié au pdf n'existe pas encore, on le crée
        if not os.path.exists(pngPath):
            os.makedirs(pngPath)

        pngFile = pngPath + f"page{pageId+1}.png"
        pagePix.writePNG(pngFile)
        pngFiles.append(pngFile)

    pdf.close()
    # On retourne la liste des pngs générés
    return pngFiles

def img2text(pngFile) :
    # On récupère le texte contenu dans l'image par extraction OCR
    detection_result = reader.detect(pngFile, width_ths=0.7, mag_ratio=1.5)
    recognition_results = reader.recognize(pngFile, horizontal_list = detection_result[0][0], free_list=[])

    textList = []
    for result in recognition_results:
        textList.append((result[1]))

    # On retourne la liste des textes extraits de l'image
    return "".join(textList)
