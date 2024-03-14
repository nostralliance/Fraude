from fastapi import FastAPI, UploadFile, File, HTTPException
import base64
import httpx
from httpx._exceptions import ReadTimeout

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
        async with httpx.AsyncClient(timeout=3600) as client:  # Augmentez ou diminuez le délai d'attente
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
            return {"message": "Traitement réussi", "date_feriee_trouvee": result["date_feriee_trouvee"], "reference_archivage_trouvee":result["reference_archivage_trouvee"], "rononsoumis_trouvee": result["rononsoumis_trouvee"], "finess_faux_trouvee": result["finess_faux_trouvee"], "adherant_suspicieux_trouvee": result["adherant_suspicieux_trouvee"], "date_superieur_trouver": result["date_superieur_trouver"], "ref_superieur_trouver": result["ref_superieur_trouver"], "blur_trouvee": result["blur_trouvee"]}
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors du traitement")

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
