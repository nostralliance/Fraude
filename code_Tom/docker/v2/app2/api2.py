#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------Bibliothèque-----------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import base64
import os
from mylib import functions, criterias
import signal
from datetime import datetime
import uuid
import shutil
from typing import List

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------variable-----------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

app = FastAPI()
# Variables globales pour les statistiques
total_factures = 0
total_ok = 0
total_ko = 0
total_taux_compare = 0
total_dateferiee = 0
total_refarchivesfaux = 0
total_rononsoumis = 0
total_finessfaux = 0
total_datecompare = 0
total_count_ref = 0
total_adherentssoussurveillance = 0
total_medical_materiel = 0
total_meta = 0




    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------plusieurs_documents------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.post('/plusieurs_documents')
async def process_file(id: List[str] = Form(...), file_path: List[UploadFile] = File(...)):
    global total_factures, total_ok, total_ko, total_taux_compare, total_dateferiee, total_refarchivesfaux, total_rononsoumis, total_finessfaux, total_datecompare, total_count_ref, total_adherentssoussurveillance, total_medical_materiel, total_meta
    results = []
    list_file_id = zip(id,file_path)
    for ident, file in list_file_id:
        total_factures += 1
        try:
            # Lire le contenu du fichier
            binary_data = await file.read()
            file_extension = criterias.detect_file_type(binary_data)

            if file_extension == 'pdf':
                pdf_file_path = f'temp_{ident}.pdf'
                with open(pdf_file_path, 'wb') as pdf_out:
                    pdf_out.write(binary_data)
                
                if criterias.detecter_fraude_documentaire(pdf_file_path):
                    total_ok += 1
                    total_meta += 1
                    results.append({"id": ident, "result": "ok", "motif": "la provenance du document est suspicieuse : photoshop, canva, excel ou word"})
                    break
                    
                pages = None
                png_files = functions.pdf2img(pdf_file_path, pages)

                for png_file in png_files:
                    print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                    png_text = functions.img2text(png_file)

                    try:
                        if criterias.finessfaux(png_text):
                            total_ok += 1
                            print('ok')
                            total_finessfaux += 1
                            result = {"id": ident, "result": "ok", "motif": "numéro finess sur facture"}
                            break

                        if criterias.adherentssoussurveillance(png_text):
                            total_ok += 1
                            print('ok')
                            total_adherentssoussurveillance += 1
                            result = {"id": ident, "result": "ok", "motif": "adherent suspicieux"}
                            break

                        if criterias.refarchivesfaux(png_text):
                            total_ok += 1
                            print('ok')
                            total_refarchivesfaux += 1
                            result = {"id": ident, "result": "ok", "motif": "reference archivage fausse sur facture"}
                            break

                        if criterias.rononsoumis(png_text):
                            total_ok += 1
                            print('ok')
                            total_rononsoumis += 1
                            result = {"id": ident, "result": "ok", "motif": "regime obligatoire non soumis sur facture"}
                            break
                            
                        
                        # png_text_list = functions.img2textlist(png_file)
                        # if criterias.date_compare(png_text_list):
                        #     total_ok += 1
                        #     total_datecompare += 1
                        #     result = {"id": ident, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"}
                        #     break
                        
                        # if criterias.medical_materiel(png_text):
                        #     total_ok += 1
                        #     print('ok')
                        #     total_medical_materiel += 1
                        #     result = {"id": ident, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"}
                        #     break

                        # if criterias.dateferiee(png_text):
                        #     total_ok += 1
                        #     print('ok')
                        #     total_dateferiee += 1
                        #     result = {"id": ident, "result": "ok", "motif": "date fériée sur facture"}
                        #     break
                        
                        else:
                            total_ko += 1
                            result = {"id": ident, "result": "ko","motif": "Pas de suspicion de fraude sur cette facture"}

                    except Exception as e:
                        print(e)
                        total_ko += 1
                        result = {"id": ident, "result": "ko", "motif": "500, erreur sur le document"}

                os.remove(pdf_file_path)
                results.append(result)

            elif file_extension in ['jpg', 'jpeg', 'png']:
                # Sauvegarder l'image dans un dossier temporaire
                temp_dir = os.path.basename(file.filename).split('.')[0]  # Utiliser le nom de fichier sans extension
                os.makedirs(temp_dir, exist_ok=True)
                file_name = f'{uuid.uuid4()}.{file_extension}'
                temp_file_path = os.path.join(temp_dir, file_name)
                with open(temp_file_path, 'wb') as out_file:
                    out_file.write(binary_data)

                # Traiter les images dans le dossier temporaire
                for img_file in os.listdir(temp_dir):
                    print("---traitement de l'image---")
                    img_path = os.path.join(temp_dir, img_file)
                    if criterias.detecter_fraude_documentaire(img_path):
                        total_ok += 1
                        total_meta += 1
                        shutil.rmtree(temp_dir)
                        results.append({"id": ident, "result": "ok", "motif": "la provenance du document est suspicieuse : photoshop, canva, excel ou word"})
                        break
                    
                    png_text = functions.img2text(img_path)
                    
                    try:
                        if criterias.finessfaux(png_text):
                            total_ok += 1
                            total_finessfaux += 1
                            print('ok')
                            shutil.rmtree(temp_dir)
                            results.append({"id": ident, "result": "ok", "motif": "numéro finess sur facture"})
                            break

                        if criterias.adherentssoussurveillance(png_text):
                            total_ok += 1
                            total_adherentssoussurveillance += 1
                            print('ok')
                            shutil.rmtree(temp_dir)
                            results.append({"id": ident, "result": "ok", "motif": "adherent suspicieux"})
                            break
                        
                        if criterias.refarchivesfaux(png_text):
                            total_ok += 1
                            total_refarchivesfaux += 1
                            print('ok')
                            shutil.rmtree(temp_dir)
                            results.append({"id": ident, "result": "ok", "motif": "reference archivage fausse sur facture"})
                            break

                        if criterias.rononsoumis(png_text):
                            total_ok += 1
                            total_rononsoumis += 1
                            print('ok')
                            shutil.rmtree(temp_dir)
                            results.append({"id": ident, "result": "ok", "motif": "regime obligatoire non soumis sur facture"})
                            break
                        
                        # png_text_list = functions.img2textlist(img_path)
                        # if criterias.date_compare(png_text_list):
                        #     total_ok += 1
                        #     total_datecompare += 1
                        #     print('ok')
                        #     shutil.rmtree(temp_dir)
                        #     results.append({"id": ident, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"})
                        #     break

                        # if criterias.medical_materiel(png_text):
                        #     total_ok += 1
                        #     total_medical_materiel += 1
                        #     print('ok')
                        #     shutil.rmtree(temp_dir)
                        #     results.append({"id": ident, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"})
                        #     break

                        # if criterias.dateferiee(png_text):
                        #     total_ok += 1
                        #     total_dateferiee += 1
                        #     print('ok')
                        #     shutil.rmtree(temp_dir)
                        #     results.append({"id": ident, "result": "ok", "motif": "date fériée sur facture"})
                        #     break

                        else:
                            total_ko += 1
                            shutil.rmtree(temp_dir)
                            results.append({"id": ident, "result": "ko","motif": "Pas de suspicion de fraude sur cette facture"})

                    except Exception as e:
                        print(f"An error occurred during criteria evaluation: {str(e)}")
                        raise HTTPException(status_code=500, detail="Internal Server Error")

            else:
                raise HTTPException(status_code=400, detail="Format de fichier non supporté")

        except Exception as e:
            total_ko += 1
            print(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"results": results}



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------plusieurs_lien_fichier------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.post('/plusieurs_liens_fichiers')
async def process_file(id: List[str] = Form(...), file_path: List[str] = Form(...)):
    global total_factures, total_ok, total_ko, total_taux_compare, total_dateferiee, total_refarchivesfaux, total_rononsoumis, total_finessfaux, total_datecompare, total_count_ref, total_adherentssoussurveillance, total_medical_materiel, total_meta
    total_factures += 1

    results = []
    list_file_id = zip(id, file_path)
    for ident, file in list_file_id:
        print(f'Les noms de fichiers sont : {file_path}')
        try:
            if not os.path.exists(file):
                raise HTTPException(status_code=400, detail="File does not exist")

            with open(file, 'rb') as file_handle:
                binary_data = file_handle.read()

            file_extension = criterias.detect_file_type(binary_data)
            result = {"id": ident, "result": "ko", "motif": "Pas de suspicion de fraude sur cette facture"}  # Default result

            if file_extension == 'pdf':
                pdf_file_path = f'temp_{ident}.pdf'
                with open(pdf_file_path, 'wb') as pdf_out:
                    pdf_out.write(binary_data)
                
                if criterias.detecter_fraude_documentaire(pdf_file_path):
                    total_ok += 1
                    total_meta += 1
                    result = {"id": ident, "result": "ok", "motif": "la provenance du document est suspicieuse : photoshop, canva, excel ou word"}
                else:
                    pages = None
                    png_files = functions.pdf2img(pdf_file_path, pages)
                    for png_file in png_files:
                        print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                        png_text = functions.img2text(png_file)
                        try:
                            if criterias.finessfaux(png_text):
                                total_ok += 1
                                print('ok')
                                total_finessfaux += 1
                                result = {"id": ident, "result": "ok", "motif": "numéro finess sur facture"}
                                break

                            if criterias.adherentssoussurveillance(png_text):
                                total_ok += 1
                                print('ok')
                                total_adherentssoussurveillance += 1
                                result = {"id": ident, "result": "ok", "motif": "adherent suspicieux"}
                                break

                            if criterias.refarchivesfaux(png_text):
                                total_ok += 1
                                print('ok')
                                total_refarchivesfaux += 1
                                result = {"id": ident, "result": "ok", "motif": "reference archivage fausse sur facture"}
                                break

                            if criterias.rononsoumis(png_text):
                                total_ok += 1
                                print('ok')
                                total_rononsoumis += 1
                                result = {"id": ident, "result": "ok", "motif": "regime obligatoire non soumis sur facture"}
                                break

                            png_text_list = functions.img2textlist(png_file)
                            if criterias.date_compare(png_text_list):
                                total_ok += 1
                                total_datecompare += 1
                                result = {"id": ident, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"}
                                break

                            if criterias.medical_materiel(png_text):
                                total_ok += 1
                                print('ok')
                                total_medical_materiel += 1
                                result = {"id": ident, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"}
                                break

                            if criterias.dateferiee(png_text):
                                total_ok += 1
                                print('ok')
                                total_dateferiee += 1
                                result = {"id": ident, "result": "ok", "motif": "date fériée sur facture"}
                                break

                        except Exception as e:
                            print(e)
                            total_ko += 1
                            result = {"id": ident, "result": "ko", "motif": "500, erreur sur le document"}
                            break

                    os.remove(pdf_file_path)

            elif file_extension in ['jpg', 'jpeg', 'png']:
                temp_dir = os.path.splitext(os.path.basename(file))[0]  # Utiliser le nom de fichier sans extension
                os.makedirs(temp_dir, exist_ok=True)
                file_name = f'{uuid.uuid4()}.{file_extension}'
                temp_file_path = os.path.join(temp_dir, file_name)
                print(temp_file_path)
                with open(temp_file_path, 'wb') as out_file:
                    out_file.write(binary_data)

                for img_file in os.listdir(temp_dir):
                    print("---Traitement de l'image ---")
                    img_path = os.path.join(temp_dir, img_file)
                    if criterias.detecter_fraude_documentaire(img_path):
                        total_ok += 1
                        total_meta += 1
                        result = {"id": ident, "result": "ok", "motif": "la provenance du document est suspicieuse : photoshop, canva, excel ou word"}
                        break

                    png_text = functions.img2text(img_path)
                    try:
                        if criterias.finessfaux(png_text):
                            total_ok += 1
                            total_finessfaux += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "numéro finess sur facture"}
                            break

                        if criterias.adherentssoussurveillance(png_text):
                            total_ok += 1
                            total_adherentssoussurveillance += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "adherent suspicieux"}
                            break

                        if criterias.refarchivesfaux(png_text):
                            total_ok += 1
                            total_refarchivesfaux += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "reference archivage fausse sur facture"}
                            break

                        if criterias.rononsoumis(png_text):
                            total_ok += 1
                            total_rononsoumis += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "regime obligatoire non soumis sur facture"}
                            break

                        png_text_list = functions.img2textlist(img_path)
                        if criterias.date_compare(png_text_list):
                            total_ok += 1
                            total_datecompare += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"}
                            break

                        if criterias.medical_materiel(png_text):
                            total_ok += 1
                            total_medical_materiel += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"}
                            break

                        if criterias.dateferiee(png_text):
                            total_ok += 1
                            total_dateferiee += 1
                            print('ok')
                            result = {"id": ident, "result": "ok", "motif": "date fériée sur facture"}
                            break

                    except Exception as e:
                        print(f"An error occurred during criteria evaluation: {str(e)}")
                        raise HTTPException(status_code=500, detail="Internal Server Error")
                
                shutil.rmtree(temp_dir)
            else:
                raise HTTPException(status_code=400, detail="Format de fichier non supporté")

            results.append(result)

        except Exception as e:
            total_ko += 1
            print(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return results

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------print_statistics------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_statistics(signal, frame):
    print(f"Total factures traitées: {total_factures}")
    print(f"Total de facture suspicieuse: {total_ok}")
    print(f"Total de facture non suspicieuse: {total_ko}")
    print(f"nombre de suspicion la différence prix/taux/total: {total_taux_compare}")
    print(f"nombre de suspicion sur la date feriee: {total_dateferiee}")
    print(f"nombre de reference d'archivage suspicieuse: {total_refarchivesfaux}")
    print(f"nombre de RO non soumis: {total_rononsoumis}")
    print(f"nombre de finess suspicieux: {total_finessfaux}")
    print(f"nombre de date de soins suspicieuse par rapport a la date de réglement: {total_datecompare}")
    print(f"nombre de reference d'archivage supérieur a 17: {total_count_ref}")
    print(f"nombre d'adherent suspicieux: {total_adherentssoussurveillance}")
    print(f"nombre de montant superieur a 150 sur facture materiel: {total_medical_materiel}")
    print(f"metadonne trouver : {total_meta}")
    print(f"a lheure:{datetime.now()}")
    exit(0)

#Ces lignes de code enregistrent une fonction pour imprimer des statistiques lorsque le programme reçoit des signaux d'interruption (Ctrl+C) ou de terminaison, afin de s'arrêter proprement.
signal.signal(signal.SIGINT, print_statistics)
signal.signal(signal.SIGTERM, print_statistics)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------lancer l'app------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
