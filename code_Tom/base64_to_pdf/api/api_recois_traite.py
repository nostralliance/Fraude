from flask import Flask, request, jsonify
from mylib import paths, functions, criterias, constants
from base64 import b64decode
import os
import json
app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    result=[]
    data = request.get_json()
    if data:
        base64_data = data.get("base64")
        pdf_data = b64decode(base64_data, validate=True)
        with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\output.pdf', 'wb') as pdf_out:
            pdf_out.write(pdf_data)
        pdfFile = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\output.pdf'
        pages = None  # traiter toutes les pages
        png_files = functions.pdf2img(pdfFile, pages)

        for pngFile in png_files:
            print("---Traitement de la page : " + os.path.basename(pngFile) + "...")
            # On récuprère le texte extrait du png
            pngText = functions.img2text(pngFile)
            result_ocr = criterias.dateferiee(pngText)
            if result_ocr == True:
                result.append(result_ocr)
                break

        result_dict = {
            "date_feriee_trouvee": bool(result),  # True si une date a été trouvée, False sinon
            }

        with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\api\result.json', 'w') as json_file:
            json.dump(result_dict, json_file)

    else:
        return jsonify({"error": "Aucune donnée JSON reçue"}), 400
    
    return jsonify({"message": "Traitement terminé"}), 200



if __name__ == '__main__':
    app.run(debug=True)
