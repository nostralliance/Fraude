import os
import csv
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path  # Import the Path class from pathlib


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



    return "csv crée"

_df = pd.read_csv(chemin_fichier_csv, sep=';',encoding="latin-1")

_df['path'] = _df['id'].apply(lambda x:  Path(dossier_images) / (str(x) + '.png'))

print(_df)

