from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from base64 import b64decode

app = Flask(__name__)

# Liste de tâches (simulée en mémoire)
tasks = []

# Route pour obtenir la liste de tâches
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Route pour ajouter une tâche
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task')
    if task:
        tasks.append(task)
        return jsonify({'message': 'Tâche ajoutée avec succès'})
    else:
        return jsonify({'error': 'Le champ "task" est requis'}, 400)

# Route pour mettre à jour une tâche
@app.route('/tasks/<int:index>', methods=['PUT'])
def update_task(index):
    if 0 <= index < len(tasks):
        data = request.get_json()
        new_task = data.get('task')
        if new_task:
            tasks[index] = new_task
            return jsonify({'message': 'Tâche mise à jour avec succès'})
        else:
            return jsonify({'error': 'Le champ "task" est requis'}, 400)
    else:
        return jsonify({'error': 'Tâche non trouvée'}, 404)

# Route pour supprimer une tâche
@app.route('/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        return jsonify({'message': f'Tâche supprimée avec succès: {deleted_task}'})
    else:
        return jsonify({'error': 'Tâche non trouvée'}, 404)
    
@app.route('/tasks/<int:index>', methods=['GET'])
def convert_to_pdf():
    base = input('rentrer votre base64 :')
    pdf_data = b64decode(base, validate=True)

    with open('output_2.pdf', 'wb') as pdf_out:
        pdf_out.write(pdf_data)
    return True
        


if __name__ == '__main__':
    app.run(debug=True)
