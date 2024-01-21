from PIL import Image, ImageFilter
import os

# Dossier source contenant les images
dossier_source = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\all_facture"

# Dossier de destination pour les images floues
dossier_destination = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture"

# Vérifier et créer le dossier de destination s'il n'existe pas
if not os.path.exists(dossier_destination):
    os.makedirs(dossier_destination)

# Parcours de tous les fichiers du dossier source
for nom_fichier in os.listdir(dossier_source):
    if nom_fichier.endswith(".jpg") or nom_fichier.endswith(".jpeg") or nom_fichier.endswith(".png"):
        chemin_image_source = os.path.join(dossier_source, nom_fichier)
        
        # Ouverture de l'image
        simg = Image.open(chemin_image_source)
        
        # Appliquer le flou avec un rayon de 10
        dimg = simg.filter(ImageFilter.GaussianBlur(radius=10))
        
        # Enregistrer l'image floue dans le dossier de destination
        chemin_image_destination = os.path.join(dossier_destination, f"{nom_fichier.split('.')[0]}_floue.jpg")
        dimg.save(chemin_image_destination)

print("Flou appliqué à toutes les images et enregistré dans le dossier de destination.")
