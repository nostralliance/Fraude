from fastapi import FastAPI, HTTPException
from mylib import paths, functions, criterias, constants
import base64
import os

app = FastAPI()

@app.post('/process_base64')
async def process_base64(data: dict):
    try:
        base64_data = data.get("base64_data")
        if not base64_data:
            raise HTTPException(status_code=400, detail="Le paramètre 'base64_data' est manquant dans le dictionnaire.")

        # Conversion de la base64 en données binaires (PDF)
        pdf_data = base64.b64decode(base64_data, validate=True)

        # Emplacement où enregistrer le fichier PDF résultant
        output_pdf_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\docker\v2\app2\output.pdf'

        with open(output_pdf_path, 'wb') as pdf_out:
            pdf_out.write(pdf_data)

        pages = None  # traiter toutes les pages
        png_files = functions.pdf2img(output_pdf_path, pages)

        result_dict = {
            "message": "Traitement réussi",
            "output_pdf_path": png_files,
        }

        return result_dict

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
