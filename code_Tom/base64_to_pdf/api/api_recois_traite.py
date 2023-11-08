from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        if data:
            base64_data = data.get("base64")
            
            # Faites ici le traitement souhaité avec les données base64, par exemple :
            processed_data = base64_data.upper()  # Convertir en majuscules
            
            # Renvoyez la réponse avec le résultat du traitement
            return jsonify({"result": processed_data}), 200
        else:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
