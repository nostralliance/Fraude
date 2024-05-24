from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import base64
import os
from mylib import functions, criterias



app = FastAPI()

############################################################## FONCTION DETECT FILE TYPE ################################################################################


def detect_file_type(data):
    if data.startswith(b'%PDF'):
        return 'pdf'
    elif data.startswith(b'\xFF\xD8'):
        return 'jpeg'
    elif data.startswith(b'\x89PNG'):
        return 'png'
    else:
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")



############################################################## ENDPOINT PROCESS BASE64 #################################################################################



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

        if file_extension == 'pdf':
            id = 1  # Vous devez définir comment obtenir ou générer cet 'id'
            pdf_file_path = f'temp_{id}.pdf'
            with open(pdf_file_path, 'wb') as pdf_out:
                pdf_out.write(binary_data)

            pages = None  # traiter toutes les pages
            png_files = functions.pdf2img(pdf_file_path, pages)

            for png_file in png_files:
                print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                png_text = functions.img2text(png_file)
                png_text_list = functions.img2textlist(png_file)

                try:
                    found_taux = criterias.taux_compare(png_text_list)
                    if found_taux:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "taux inexacte sur facture"
                        }

                    found_date = criterias.dateferiee(png_text)
                    if found_date:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "date fériée sur facture"
                        }

                    found_ref_archives = criterias.refarchivesfaux(png_text)
                    if found_ref_archives:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "reference archivage fausse sur facture"
                        }

                    found_non_soumis = criterias.rononsoumis(png_text)
                    if found_non_soumis:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "regime obligatoire non soumis sur facture"
                        }

                    found_finess = criterias.finessfaux(png_text)
                    if found_finess:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "numéro finess sur facture"
                        }

                    found_date_compare = criterias.date_compare(png_text_list)
                    if found_date_compare:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "date reglement supérieur a date de soins sur facture"
                        }

                    found_count_ref = criterias.count_ref(png_text_list)
                    if found_count_ref:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "reference archivage superieur a 17"
                        }

                    found_adherant = criterias.adherentssuspicieux(png_text)
                    if found_adherant:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "adherent suspicieux"
                        }

                    found_mat_med = criterias.medical_materiel(png_text)
                    if found_mat_med:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "montant superieur a 150 euros sur facture medical"
                        }

                except Exception as e:
                    print(f"An error occurred during criteria evaluation: {str(e)}")
                    raise HTTPException(status_code=500, detail="Internal Server Error")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




############################################################## ENDPOINT PROCESS FILE ###################################################################################





@app.post('/process_file')
async def process_file(id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Lire le fichier téléchargé
        binary_data = await file.read()
        file_extension = detect_file_type(binary_data)





############################################################## TRAITEMENT SUR PDF ###################################################################################


        if file_extension == 'pdf':
            pdf_file_path = f'temp_{id}.pdf'
            with open(pdf_file_path, 'wb') as pdf_out:
                pdf_out.write(binary_data)

            pages = None  # traiter toutes les pages
            png_files = functions.pdf2img(pdf_file_path, pages)

            for png_file in png_files:
                print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                png_text = functions.img2text(png_file)
                png_text_list = functions.img2textlist(png_file)

                try:
                    found_taux = criterias.taux_compare(png_text_list)
                    if found_taux:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "taux inexacte sur facture"
                        }

                    found_date = criterias.dateferiee(png_text)
                    if found_date:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "date fériée sur facture"
                        }

                    found_ref_archives = criterias.refarchivesfaux(png_text)
                    if found_ref_archives:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "reference archivage fausse sur facture"
                        }

                    found_non_soumis = criterias.rononsoumis(png_text)
                    if found_non_soumis:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "regime obligatoire non soumis sur facture"
                        }

                    found_finess = criterias.finessfaux(png_text)
                    if found_finess:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "numéro finess sur facture"
                        }

                    found_date_compare = criterias.date_compare(png_text_list)
                    if found_date_compare:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "date reglement supérieur a date de soins sur facture"
                        }

                    found_count_ref = criterias.count_ref(png_text_list)
                    if found_count_ref:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "reference archivage superieur a 17"
                        }

                    found_adherant = criterias.adherentssuspicieux(png_text)
                    if found_adherant:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "adherent suspicieux"
                        }

                    found_mat_med = criterias.medical_materiel(png_text)
                    if found_mat_med:
                        return {
                            "id": id,
                            "result": "ok",
                            "motif": "montant superieur a 150 euros sur facture medical"
                        }

                except Exception as e:
                    print(f"An error occurred during criteria evaluation: {str(e)}")
                    raise HTTPException(status_code=500, detail="Internal Server Error")

            # Suppression des fichiers temporaires
            os.remove(pdf_file_path)
            for png_file in png_files:
                os.remove(png_file)



############################################################## TRAITEMENT SUR IMAGE ###################################################################################



        elif file_extension in ['jpg', 'jpeg', 'png']:
            png_text = functions.img2text(binary_data)
            png_text_list = functions.img2textlist(binary_data)

            try:
                found_taux = criterias.taux_compare(png_text_list)
                if found_taux:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "taux inexacte sur facture"
                    }

                found_date = criterias.dateferiee(png_text)
                if found_date:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "date fériée sur facture"
                    }

                found_ref_archives = criterias.refarchivesfaux(png_text)
                if found_ref_archives:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "reference archivage fausse sur facture"
                    }

                found_non_soumis = criterias.rononsoumis(png_text)
                if found_non_soumis:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "regime obligatoire non soumis sur facture"
                    }

                found_finess = criterias.finessfaux(png_text)
                if found_finess:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "numéro finess sur facture"
                    }

                found_date_compare = criterias.date_compare(png_text_list)
                if found_date_compare:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "date reglement supérieur a date de soins sur facture"
                    }

                found_count_ref = criterias.count_ref(png_text_list)
                if found_count_ref:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "reference archivage superieur a 17"
                    }

                found_adherant = criterias.adherentssuspicieux(png_text)
                if found_adherant:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "adherent suspicieux"
                    }

                found_mat_med = criterias.medical_materiel(png_text)
                if found_mat_med:
                    return {
                        "id": id,
                        "result": "ok",
                        "motif": "montant superieur a 150 euros sur facture medical"
                    }

            except Exception as e:
                print(f"An error occurred during criteria evaluation: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté")

        # Si aucun critère n'a été trouvé, retourner le résultat avec l'ID
        return {"id": id, "result": "ko"}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")











if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
