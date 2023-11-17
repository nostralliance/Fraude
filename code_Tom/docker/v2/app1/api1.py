from fastapi import FastAPI, UploadFile, File, HTTPException
import base64
import httpx

app = FastAPI()

# URL du service de traitement (deuxième API)
SERVICE_URL = "http://localhost:8001/process_base64"  # Remplacez par l'URL réelle de votre deuxième API

@app.post("/upload_and_process")
async def upload_and_process(pdf: UploadFile = File(...)):
    try:
        # Lecture du contenu du fichier PDF
        pdf_content = await pdf.read()

        # Conversion en base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Appel à la deuxième API pour le traitement
        async with httpx.AsyncClient() as client:
            response = await client.post(SERVICE_URL, json={"base64_data": pdf_base64})

        # Vérification de la réponse du service de traitement
        if response.status_code == 200:
            result = response.json()
            return {"message": "Traitement réussi", "result": result}
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors du traitement")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
