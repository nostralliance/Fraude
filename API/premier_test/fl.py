from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Définissez le répertoire où se trouvent vos fichiers PDF
pdf_directory = r"C:\Users\pierrontl\Documents\code_python\API"

@app.route('/recup-pdf', methods=['GET'])
def recup_pdf():
    requested_pdf = request.args.get('pdf_filename')  # Ajoutez une variable dans la requete pour obtenir le nom du fichier PDF demandé

    if requested_pdf:
        chemin_pdf = os.path.join(pdf_directory, requested_pdf)
        
        if os.path.exists(chemin_pdf) and chemin_pdf.endswith(".pdf"):
            # Renvoyez le résultat en tant que réponse JSON
            return jsonify({'resultat': chemin_pdf})
        else:
            return jsonify({'error': 'Fichier PDF non trouve'})
    else:
        return jsonify({'error': 'Parametre pdf_filename manquant dans la requete'})

if __name__ == '__main__':
    app.run(debug=True)
