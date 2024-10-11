import json
from PIL import Image, ExifTags
from datetime import datetime

def extraire_metadonnees_image(image_path):
    """
    Fonction pour extraire et afficher les métadonnées d'une image, y compris les dates de création et de modification.
    """
    try:
        # Ouvrir l'image et extraire les métadonnées Exif
        with Image.open(image_path) as img:
            image_exif = img._getexif()

            # Vérifier si les métadonnées Exif sont présentes
            if image_exif:
                # Créer un dictionnaire avec les noms des tags Exif et leurs valeurs
                exif = {ExifTags.TAGS.get(k, k): v for k, v in image_exif.items() if k in ExifTags.TAGS and isinstance(v, (str, int, float))}
                
                # Afficher les métadonnées sous forme JSON
                print("Métadonnées de l'image :")
                print(json.dumps(exif, indent=4))

                # Extraire les dates si elles sont présentes
                date_creation = exif.get('DateTimeOriginal', None)
                date_modification = exif.get('DateTime', None)

                # Afficher les dates de création et de modification
                if date_creation:
                    try:
                        date_obj_creation = datetime.strptime(date_creation, '%Y:%m:%d %H:%M:%S')
                        print(f"\nDate de création de l'image : {date_obj_creation}")
                    except ValueError:
                        print(f"\nDate de création de l'image (format non valide) : {date_creation}")
                else:
                    print("\nDate de création de l'image non trouvée.")

                if date_modification:
                    try:
                        date_obj_modification = datetime.strptime(date_modification, '%Y:%m:%d %H:%M:%S')
                        print(f"Date de modification de l'image : {date_obj_modification}")
                    except ValueError:
                        print(f"Date de modification de l'image (format non valide) : {date_modification}")
                else:
                    print("Date de modification de l'image non trouvée.")
            else:
                print("Aucune métadonnée trouvée pour cette image.")

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées : {e}")

# Exemple d'utilisation
image_path = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\multi_training\bdd_photoshop\SKM_30823122012370pdf_page_2.jpg"
extraire_metadonnees_image(image_path)
