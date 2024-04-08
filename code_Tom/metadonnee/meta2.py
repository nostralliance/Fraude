from PIL import Image
from PIL.ExifTags import TAGS

def extraire_metadonnees_image(image_path):
    """
    Fonction pour extraire les métadonnées d'une image.
    """
    # Ouvrir l'image
    with Image.open(image_path) as img:
        # Extraire les métadonnées
        metadata = img._getexif()

        # Afficher les métadonnées
        if metadata:
            print("Métadonnées de l'image :")
            for tag, value in metadata.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print("Aucune métadonnée trouvée pour cette image.")

# Exemple d'utilisation
image_path = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\metadonnee\test_pdf\sharp\test1.png"
#C:\Users\ilboudob\Downloads\factures o tester
extraire_metadonnees_image(image_path)