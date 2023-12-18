from fastapi import FastAPI, HTTPException, UploadFile, File
import base64
import io
from PIL import Image
from mylib import paths, functions, criterias, constants
import os
import argparse

app = FastAPI()

@app.post('/process_base64')
async def process_base64(data: dict):
    try:
        base64_data = data.get("base64_data")
        if not base64_data:
            raise HTTPException(status_code=400, detail="Le paramètre 'base64_data' est manquant dans le dictionnaire.")

        # Conversion de la base64 en données binaires
        binary_data = base64.b64decode(base64_data, validate=True)

        # Détection du type de fichier
        file_extension = detect_file_type(binary_data)
        list_result_dateferiee = []
        list_result_refarchives = []
        list_result_nonsoumis = []
        list_blur = []

        if file_extension == 'pdf':
            with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\fastapi\output.pdf', 'wb') as pdf_out:
                pdf_out.write(binary_data)

                pdf_file = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\fastapi\output.pdf'

                pages = None  # traiter toutes les pages
                png_files = functions.pdf2img(pdf_file, pages)
                for png_file in png_files:
                    print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                    blur = criterias.is_image_blurry(png_file, threshold_scale=0.0001)
                    print(blur)
                    # On récupère le texte extrait du png
                    png_text = functions.img2text(png_file)
                    print("le texte est :", png_text)
                    result_ocr = criterias.dateferiee(png_text)
                    result_refarchivesfaux = criterias.refarchivesfaux(png_text)
                    result_rononsoumis = criterias.rononsoumis(png_text)
                    # print(result_refarchivesfaux)
                    if result_ocr:
                        list_result_dateferiee.append(result_ocr)
                        break
                    elif result_refarchivesfaux:
                        list_result_refarchives.append(result_refarchivesfaux)
                        break
                    elif result_rononsoumis:
                        list_result_nonsoumis.append(result_rononsoumis)
                        break
                    elif blur:
                        list_blur.append(blur)


        elif file_extension in ['jpg', 'jpeg', 'png']:
            # Traitement de l'image directement
            print("---Traitement de l'image---")
            png_text = functions.img2text(binary_data)
            result_refarchivesfaux = criterias.refarchivesfaux(png_text)
            result_rononsoumis = criterias.rononsoumis(png_text)
            # print(result_refarchivesfaux)
            # print(png_text)
            result_ocr = criterias.dateferiee(png_text)
            if result_ocr:
                list_result_dateferiee.append(result_ocr)
            elif result_refarchivesfaux:
                list_result_refarchives.append(result_refarchivesfaux)
            elif result_rononsoumis:
                list_result_nonsoumis.append(result_rononsoumis)
            elif blur:
                list_blur.append(blur)

        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté")

        result_dict = {
            "date_feriee_trouvee": bool(list_result_dateferiee),  # True si une date a été trouvée, False sinon
            "reference_archivage_trouvee": bool(list_result_refarchives),
            "rononsoumis_trouvee": bool(list_result_nonsoumis),
            "blur_trouvee": blur

        }

        return result_dict

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def detect_file_type(data):
    # Déterminer le type de fichier en fonction de l'en-tête
    if data.startswith(b'%PDF'):
        return 'pdf'
    elif data.startswith(b'\xFF\xD8'):
        return 'jpeg'
    elif data.startswith(b'\x89PNG'):
        return 'png'
    else:
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
