import os
import csv
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

dossier_images = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\Tests-Ben-TMP"
chemin_fichier_csv = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data.csv"

noms_images = []

def create_csv():
    for nom_fichier in os.listdir(dossier_images):
        if nom_fichier.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            noms_images.append(nom_fichier)

    with open(chemin_fichier_csv, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        
        # Écriture de l'en-tête du CSV
        writer.writerow(["id"])

        # Écriture des noms d'images sans l'extension .png
        for nom_image in noms_images:
            nom_base, extension = os.path.splitext(nom_image)
            if extension.lower() == '.png':
                nom_image_affiche = nom_base
            else:
                nom_image_affiche = nom_image
            writer.writerow([nom_image_affiche])

    _df = pd.read_csv(chemin_fichier_csv, sep=';',encoding="latin-1")

   
    _df['path'] = _df['Id'].apply(lambda x:  chemin_fichier_csv.Path('Tests-Ben-TMP') / (str(x) + '.png'))

    return _df


# choix = input('choisissez : \n 1. afficher dataset\n 2. describe\n 3. info\n 4. cree dataset\n')

# df = pd.read_csv(chemin_fichier_csv, sep=";", encoding='latin-1')

# Afficher chaque image
# if choix == "1":
#     for index, row in df.iterrows():
#         nom_image = row["Nom de l'image"]
#         chemin_image = os.path.join(dossier_images, nom_image)

#         # Charger et afficher l'image
#         image = Image.open(chemin_image)
#         plt.imshow(image)

#         # Obtenir le nom de base du fichier sans l'extension .png
#         nom_base, extension = os.path.splitext(nom_image)
#         if extension.lower() == '.png':
#             nom_image_affiche = nom_base
#         else:
#             nom_image_affiche = nom_image

#         plt.title(f"Image {index + 1}: {nom_image_affiche}")
#         plt.show()


# elif choix == "2":
#     print(df.describe())

# elif choix == "3":
#     print(df.info())
# elif choix == "4":
create_csv()


