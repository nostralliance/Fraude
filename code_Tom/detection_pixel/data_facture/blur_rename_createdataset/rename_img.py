import os

def rename_images(input_folder):
    # Assurez-vous que le dossier d'entrée existe
    if not os.path.exists(input_folder):
        print(f"Le dossier {input_folder} n'existe pas.")
        return

    # Liste des extensions d'image prises en charge
    image_extensions = ['.jpg', '.jpeg', '.png']

    # Filtrez les fichiers pour ne récupérer que ceux avec les extensions d'image
    image_files = [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in image_extensions)]

    # Parcourez les fichiers et renommez-les
    for idx, filename in enumerate(image_files, start=1):
        # Chemin complet du fichier d'origine
        old_path = os.path.join(input_folder, filename)

        # Obtenez l'extension du fichier
        _, file_extension = os.path.splitext(filename)

        # Nouveau nom de fichier avec un numéro séquentiel, "blur" et l'extension d'origine
        new_filename = f"{idx}blur{file_extension}"

        # Chemin complet du fichier renommé
        new_path = os.path.join(input_folder, new_filename)

        # Renommez le fichier
        os.rename(old_path, new_path)
        print(f"Fichier renommé : {old_path} -> {new_path}")

# Exemple d'utilisation :
input_folder = r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\blurv5'
rename_images(input_folder)
