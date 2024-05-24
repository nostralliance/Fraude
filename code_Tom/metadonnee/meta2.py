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
image_path = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\docker\v2\app1\SKM_30823122012370.pdf_page_1.jpg"
#C:\Users\ilboudob\Downloads\factures o tester
extraire_metadonnees_image(image_path)