import requests
import base64
from PIL import Image
from io import BytesIO
# URL du service web
base_url = 'http://localhost:5000/tasks'

# Fonction pour afficher la liste des tâches
def get_tasks():
    response = requests.get(base_url)
    if response.status_code == 200:
        tasks = response.json().get('tasks')
        if tasks:
            print("Liste des tâches :")
            for index, task in enumerate(tasks):
                print(f"{index}: {task}")
        else:
            print("Aucune tâche trouvée.")
    else:
        print(f"Erreur {response.status_code}: Impossible de récupérer la liste des tâches.")

# Fonction pour ajouter une nouvelle tâche
def add_task(task_text):
    data = {'task': task_text}
    response = requests.post(base_url, json=data)
    if response.status_code == 200:
        print("Tâche ajoutée avec succès.")
    else:
        print(f"Erreur {response.status_code}: Impossible d'ajouter la tâche.")

# Fonction pour mettre à jour une tâche existante
def update_task(index, new_task_text):
    url = f'{base_url}/{index}'
    data = {'task': new_task_text}
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print("Tâche mise à jour avec succès.")
    else:
        print(f"Erreur {response.status_code}: Impossible de mettre à jour la tâche.")

# Fonction pour supprimer une tâche existante
def delete_task(index):
    url = f'{base_url}/{index}'
    response = requests.delete(url)
    if response.status_code == 200:
        print("Tâche supprimée avec succès.")
    else:
        print(f"Erreur {response.status_code}: Impossible de supprimer la tâche.")

# Fonction pour convertir une image base64 en image normale
def convert_img(index):
    url = f'{base_url}/{index}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Image convertie et enregistrée avec succès.")
    else:
        print(f"Erreur {response.status_code}: Impossible de convertir l'image.")



# Exemple d'utilisation de l'application cliente
if __name__ == '__main__':
    print("Bienvenue dans l'application cliente de gestion de tâches.")
    while True:
        print("\nOptions disponibles:")
        print("1. Afficher la liste des tâches")
        print("2. Ajouter une nouvelle tâche")
        print("3. Mettre à jour une tâche")
        print("4. Supprimer une tâche")
        print("5. convertir une image base 64")
        print("0. Quitter")
        choice = input("Sélectionnez une option (0-5) : ")

        if choice == '1':
            get_tasks()
        elif choice == '2':
            task_text = input("Entrez le texte de la nouvelle tâche : ")
            add_task(task_text)
        elif choice == '3':
            index = int(input("Entrez l'index de la tâche à mettre à jour : "))
            new_task_text = input("Entrez le nouveau texte de la tâche : ")
            update_task(index, new_task_text)
        elif choice == '4':
            index = int(input("Entrez l'index de la tâche à supprimer : "))
            delete_task(index)
        elif choice == '5':
            index = input("Entrez l'index de l'image a convertir : ")
            convert_img(index)
        elif choice == '0':
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez sélectionner une option valide.")
