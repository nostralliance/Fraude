from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import easyocr
import io
import requests
import fitz, os
import easyocr
from typing import Tuple
#import ocrmypdf
import io

app = FastAPI()
reader = easyocr.Reader(['en', 'fr'], gpu=False)

def img2text(image_content):
    # Detect text in the image using OCR
    detection_result = reader.detect(image_content, width_ths=0.7, mag_ratio=1.5)
    recognition_results = reader.recognize(image_content, horizontal_list=detection_result[0][0], free_list=[])

    textList = []
    for result in recognition_results:
        textList.append(result[1])

    # Return the list of extracted texts from the image
    return " ".join(textList)




# def pdf2img( pdfFile: str ,pages: Tuple = None):
#     # On charge le document
#     pdf = fitz.open(pdfFile)
#     # On détermine la liste des fichiers générés
#     pngFiles = []
#     # Pour chaque page du pdf
#     for pageId in range(pdf.pageCount):

#         if str(pages) != str(None):
#             if str(pageId) not in str(pages):
#                 continue

#         # On récupère la page courante
#         page = pdf[pageId]
#         # On convertit la page courante
#         pageMatrix = fitz.Matrix(2, 2).preRotate(int(0))
#         pagePix = page.getPixmap(matrix=pageMatrix, alpha=False)
#         # On exporte la page générée
#         pngPath = 'OCR/' + os.path.basename(pdfFile) +'/'
#         # Si le répertoire dédié au pdf n'existe pas encore, on le crée
#         if not os.path.exists(pngPath):
#             os.makedirs(pngPath)

#         pngFile = pngPath + f"page{pageId+1}.png"
#         pagePix.writePNG(pngFile)
#         pngFiles.append(pngFile)

#     pdf.close()
#     # On retourne la liste des pngs générés
#     return pngFiles





@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read the image file and extract text
        #print(file)
        #if file.filename.endswith('.pdf'):
            #pdf = await file.read()
            #pdftoimage= pdf2img(pdf)

       # else: 
            image_content = await file.read()
            print(type(image_content))
        #print(image_content)
            extracted_text = img2text(image_content)
            return JSONResponse(content={"text": extracted_text})
        

    except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)