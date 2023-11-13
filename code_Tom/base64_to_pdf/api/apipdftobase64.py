from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

# Route pour télécharger le fichier PDF
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        pdf_file = request.files['pdf']
        if pdf_file:
            # Lire le contenu du fichier PDF
            pdf_content = pdf_file.read()

            # Convertir le contenu en base64
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

            # Créer un dictionnaire JSON avec la donnée base64
            data = {"base64": pdf_base64}
            print(data)
            # Envoyer le JSON à l'autre API
            response = send_data_to_other_api(data)

            return jsonify({"message": "Fichier PDF traité avec succès et envoyé à l'autre API"}), 200
        else:
            return jsonify({"error": "Aucun fichier PDF n'a été téléchargé"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fonction pour envoyer le JSON à l'autre API
def send_data_to_other_api(data):
    try:
        other_api_url = "http://127.0.0.1:5000/process_json"  # Remplacez ceci par l'URL de l'autre API
        headers = {'Content-Type': 'application/json'}
        response = requests.post(other_api_url, json=data, headers=headers) # header on met des token dedans autorisation

        if response.status_code == 200:
            print(response)
            return response.json()
        else:
            return {"error": "Échec de l'envoi des données à l'autre API"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
