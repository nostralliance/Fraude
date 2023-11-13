from fastapi import FastAPI, UploadFile, File, HTTPException
from mylib import paths, functions, criterias, constants
import base64
import requests
import json
import os
import uvicorn


app = FastAPI()

# Variable globale pour stocker la base64
global_base64_data = None

# Route pour télécharger le fichier PDF
@app.post("/upload_pdf")
async def upload_pdf(pdf: UploadFile = File(...)):
    global global_base64_data
    try:
        pdf_content = await pdf.read()
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Stocker la base64 dans la variable globale
        global_base64_data = {"base64": pdf_base64}

        return {"message": global_base64_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post('/process_base64')
async def process_base64():
    global global_base64_data
    try:
        if global_base64_data is None:
            raise HTTPException(status_code=400, detail="Base64 data is missing")

        base64_data = global_base64_data.get("base64")
        pdf_data = base64.b64decode(base64_data, validate=True)

        with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\fastapi\output.pdf', 'wb') as pdf_out:
            pdf_out.write(pdf_data)

        pdf_file = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\fastapi\output.pdf'

        pages = None  # traiter toutes les pages
        png_files = functions.pdf2img(pdf_file, pages)

        result = []
        for png_file in png_files:
            print("---Traitement de la page : " + os.path.basename(png_file) + "...")
            # On récupère le texte extrait du png
            png_text = functions.img2text(png_file)
            result_ocr = criterias.dateferiee(png_text)
            if result_ocr:
                result.append(result_ocr)
                break

        result_dict = {
            "date_feriee_trouvee": bool(result),  # True si une date a été trouvée, False sinon
        }

        return result_dict

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    uvicorn.run(app)
