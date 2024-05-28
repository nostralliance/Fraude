from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import base64
import os
from mylib import functions, criterias
import signal
from datetime import datetime

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
total_metadonne = 0



@app.post('/process_file')
async def process_file(id: str = Form(...), file: UploadFile = File(...)):
    global total_factures, total_ok, total_ko, total_taux_compare, total_dateferiee, total_refarchivesfaux, total_rononsoumis, total_finessfaux, total_datecompare, total_count_ref, total_adherentssoussurveillance, total_medical_materiel, total_metadonne
    total_factures += 1
    try:
        binary_data = await file.read()
        file_extension = criterias.detect_file_type(binary_data)

        if file_extension == 'pdf':
            pdf_file_path = f'temp_{id}.pdf'
            with open(pdf_file_path, 'wb') as pdf_out:
                pdf_out.write(binary_data)
            
            if criterias.detecter_fraude_documentaire(pdf_file_path):
                total_ok += 1
                total_metadonne += 1
                return {"id": id, "result": "ok", "motif": "la provenance du document est suspicieuse : photoshop, canva, excel ou word"}
                

            pages = None
            png_files = functions.pdf2img(pdf_file_path, pages)

            for png_file in png_files:
                print("---Traitement de la page : " + os.path.basename(png_file) + "...")
                png_text = functions.img2text(png_file)
                png_text_list = functions.img2textlist(png_file)

                try:
                    if criterias.finessfaux(png_text):
                        total_ok += 1
                        total_finessfaux += 1
                        return {"id": id, "result": "ok", "motif": "numéro finess sur facture"}
                        break

                    if criterias.adherentssoussurveillance(png_text):
                        total_ok += 1
                        total_adherentssoussurveillance += 1
                        return {"id": id, "result": "ok", "motif": "adherent suspicieux"}
                    
                    if criterias.refarchivesfaux(png_text):
                        total_ok += 1
                        total_refarchivesfaux += 1
                        return {"id": id, "result": "ok", "motif": "reference archivage fausse sur facture"}
                        break

                    if criterias.rononsoumis(png_text):
                        total_ok += 1
                        total_rononsoumis += 1
                        return {"id": id, "result": "ok", "motif": "regime obligatoire non soumis sur facture"}
                        break
                    
                    if criterias.date_compare(png_text_list):
                        total_ok += 1
                        total_datecompare += 1
                        return {"id": id, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"}
                    
                    if criterias.medical_materiel(png_text):
                        total_ok += 1
                        total_medical_materiel += 1
                        return {"id": id, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"}

                    if criterias.dateferiee(png_text):
                        total_ok += 1
                        total_dateferiee =+ 1
                        return {"id": id, "result": "ok", "motif": "date fériée sur facture"}
                        break

                except Exception as e:
                    total_ko += 1
                    return {"id": id, "result": "ko", "motif": "500, erreur sur le document"}

            os.remove(png_files)

        elif file_extension in ['jpg', 'jpeg', 'png']:
            png_text = functions.img2text(binary_data)
            png_text_list = functions.img2textlist(binary_data)

            try:
                if criterias.finessfaux(png_text):
                    total_ok += 1
                    total_finessfaux += 1
                    return {"id": id, "result": "ok", "motif": "numéro finess sur facture"}
                    break

                if criterias.adherentssoussurveillance(png_text):
                    total_ok += 1
                    total_adherentssoussurveillance += 1
                    return {"id": id, "result": "ok", "motif": "adherent suspicieux"}
                
                if criterias.refarchivesfaux(png_text):
                    total_ok += 1
                    total_refarchivesfaux += 1
                    return {"id": id, "result": "ok", "motif": "reference archivage fausse sur facture"}
                    break

                if criterias.rononsoumis(png_text):
                    total_ok += 1
                    total_rononsoumis += 1
                    return {"id": id, "result": "ok", "motif": "regime obligatoire non soumis sur facture"}
                    break
                
                if criterias.date_compare(png_text_list):
                    total_ok += 1
                    total_datecompare += 1
                    return {"id": id, "result": "ok", "motif": "date reglement supérieur a date de soins sur facture"}
                
                if criterias.medical_materiel(png_text):
                    total_ok += 1
                    total_medical_materiel += 1
                    return {"id": id, "result": "ok", "motif": "montant superieur a 150 euros sur facture medical"}

                if criterias.dateferiee(png_text):
                    total_ok += 1
                    total_dateferiee =+ 1
                    return {"id": id, "result": "ok", "motif": "date fériée sur facture"}
                    break
            except Exception as e:
                print(f"An error occurred during criteria evaluation: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

            total_ko += 1
            return {"id": id, "result": "ko"}

        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté")

    except Exception as e:
        total_ko += 1
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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
    print("metadonne trouver : {total_metadonne}")
    print(f"a lheure:{datetime.now()}")
    exit(0)

#Ces lignes de code enregistrent une fonction pour imprimer des statistiques lorsque le programme reçoit des signaux d'interruption (Ctrl+C) ou de terminaison, afin de s'arrêter proprement.
signal.signal(signal.SIGINT, print_statistics)
signal.signal(signal.SIGTERM, print_statistics)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
