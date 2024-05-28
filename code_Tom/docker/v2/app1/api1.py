from fastapi import FastAPI, UploadFile, File, HTTPException
import base64
import httpx
from httpx._exceptions import ReadTimeout
import uvicorn

app = FastAPI()

# URL du service de traitement (deuxième API)
SERVICE_URL = "http://localhost:8001/process_base64"

@app.post("/upload_and_process")
async def upload_and_process(pdf: UploadFile = File(...)):
    try:
        # Lecture du contenu du fichier PDF
        pdf_content = await pdf.read()

        # Conversion en base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Appel à la deuxième API pour le traitement
        async with httpx.AsyncClient(timeout=900) as client:
            try:
                response = await client.post(SERVICE_URL, json={"base64_data": pdf_base64})
                response.raise_for_status()
            except ReadTimeout as e:
                raise HTTPException(status_code=504, detail="Timeout lors de l'appel à la deuxième API")
            except httpx.HTTPError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Vérification de la réponse du service de traitement
        if response.status_code == 200:
            result = response.json()
            print("resultat :", result)
            
            if result["result"] == "ok":
                return {"message": result}
            else:
                return {"message": "Traitement réussi", "result": "ko"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors du traitement")

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
