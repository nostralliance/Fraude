import re 
import pandas as pd
from datetime import date
from jours_feries_france import JoursFeries 
from dateutil.relativedelta import relativedelta 
# from autocorrect import Speller
import cv2 
import argparse
# from imutils import paths
from datetime import datetime
import numpy as np 
from PIL import Image
from PIL.ExifTags import TAGS
import fitz  # PyMuPDF
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form

def detecter_fraude_documentaire(pdf_path):
    """
    Fonction pour détecter la fraude documentaire dans un fichier PDF.
    """
   
    extension = os.path.splitext(pdf_path)[1].lower()
    if extension == '.pdf':
    # Ouvrir le fichier PDF
        document = fitz.open(pdf_path)
 
    # Extraire les métadonnées
        metadata = document.metadata
        liste=[]
    # Vérifier la présence de métadonnées suspects
        for key, value in metadata.items():
            if isinstance(value, bytes):
                value = value.decode("utf-8", "ignore")
            print(f"{key}: {value}")
        #print(metadata['producer'])
            liste.append(metadata['producer'])
            liste.append(metadata['creator'])
            resultat = ' '.join(liste)
            regimeList = re.findall(r'[C|c][A|a][n|N][v|V][A|a]|[P|p][H|h][o|O][t|T][H|h][O|o][S|s][H|h][O|o][P|p]|[W|w][O|o][R|r][D|d]|[E|e][X|x][C|c][e|E][L|l]', resultat)
            if len(regimeList)> 1:
                return True
                break
            else:
                return False
           
    if extension in ('.jpg', '.jpeg', '.png'):
        liste_img=[]
        with Image.open(pdf_path) as img:
        # Extraire les métadonnées
            metadata = img._getexif()
            if metadata:
                for tag, value in metadata.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name}: {value}")
                    liste_img.append(metadata['Software'])
                    #liste.append(metadata['creator'])
                    resultat = ' '.join(liste)
                    regimeList = re.findall(r'[C|c][A|a][n|N][v|V][A|a]|[P|p][H|h][o|O][t|T][H|h][O|o][S|s][H|h][O|o][P|p]|[W|w][O|o][R|r][D|d]|[E|e][X|x][C|c][e|E][L|l]', resultat)
                    if len(regimeList)> 1:
                        return True
                        break
                    else:
                        return False


detecter_fraude_documentaire(r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\multi_training\bdd_photoshopSKM_30823122012370.pdf_page_1.jpg")