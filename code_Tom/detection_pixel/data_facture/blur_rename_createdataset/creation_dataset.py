import os
import csv
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

dossier_images = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\blur"
chemin_fichier_csv = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\data_train.csv"

noms_images = []

def create_csv():
    for nom_fichier in os.listdir(dossier_images):
        if nom_fichier.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            noms_images.append(nom_fichier)

    # Vérifier si le fichier CSV existe déjà
    if os.path.exists(chemin_fichier_csv):
        # Lire le fichier CSV existant
        existing_data = pd.read_csv(chemin_fichier_csv)

        # Obtenir la liste des noms de colonnes existantes
        existing_columns = existing_data.columns.tolist()

        # Utiliser la première colonne si elle existe, sinon en créer une nouvelle
        column_name = existing_columns[0] if existing_columns else "id"

        # Obtenir la liste des noms d'images existants
        existing_image_names = existing_data[column_name].tolist()

        # Ajouter de nouvelles images qui ne sont pas déjà dans le CSV
        for nom_image in noms_images:
            nom_base, extension = os.path.splitext(nom_image)
            if extension.lower() == '.png':
                nom_image_affiche = nom_base
            else:
                nom_image_affiche = nom_image

            if nom_image_affiche not in existing_image_names:
                existing_data = existing_data.append({column_name: nom_image_affiche}, ignore_index=True)

        # Écrire les données mises à jour dans le fichier CSV
        existing_data.to_csv(chemin_fichier_csv, index=False)
    else:
        # Créer un nouveau fichier CSV s'il n'existe pas
        with open(chemin_fichier_csv, 'w', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            
            # Écriture de l'en-tête du CSV
            writer.writerow([column_name])

            # Écriture des noms d'images sans l'extension .png
            for nom_image in noms_images:
                nom_base, extension = os.path.splitext(nom_image)
                if extension.lower() == '.png':
                    nom_image_affiche = nom_base
                else:
                    nom_image_affiche = nom_image
                writer.writerow([nom_image_affiche])

    return "CSV créé"

create_csv()
