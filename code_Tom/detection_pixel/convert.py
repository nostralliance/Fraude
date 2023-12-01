from PIL import Image
import os

def rotate_images_in_folder(folder_path):
    # Assurez-vous que le chemin du dossier est absolu
    folder_path = os.path.abspath(folder_path)

    # Vérifiez si le dossier existe
    if not os.path.exists(folder_path):
        print(f"Le dossier '{folder_path}' n'existe pas.")
        return

    # Liste des extensions d'images supportées
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Vérifier si le fichier est une image
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in supported_extensions):
            # Charger l'image
            original_image = Image.open(file_path)

            # Effectuer la rotation de 90 degrés
            rotated_image = original_image.rotate(-90)

            # Construire un nouveau chemin pour l'image rotatée
            rotated_file_path = os.path.join(folder_path, f"rotated_-90_{filename}")

            # Enregistrer l'image rotatée sans écraser l'originale
            rotated_image.save(rotated_file_path)

            # Fermer les images pour libérer la mémoire
            original_image.close()
            rotated_image.close()

    print("Rotation terminée.")

# Exemple d'utilisation avec un chemin de dossier spécifique
folder_path_to_rotate = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\images_fausses"
rotate_images_in_folder(folder_path_to_rotate)
