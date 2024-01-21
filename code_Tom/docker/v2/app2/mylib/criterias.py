import re 
import pandas as pd
from . import constants,paths
from datetime import date
from jours_feries_france import JoursFeries
from dateutil.relativedelta import relativedelta
from autocorrect import Speller
import cv2
import argparse
from imutils import paths



def is_image_blurry(image_path, threshold_scale=1.0):
    # Charger l'image en niveaux de gris
    image = cv2.imread(image_path)

    # Vérifier si l'image a été lue correctement
    if image is None:
        print(f"Erreur de lecture de l'image : {image_path}")
        return False

    # Calculer la variance du gradient
    variance = cv2.Laplacian(image, cv2.CV_64F).var()

    # Ajuster le seuil en fonction de la résolution de l'image
    resolution_threshold = threshold_scale * image.size

    # Si la variance est inférieure au seuil, l'image est considérée comme floue
    return variance < resolution_threshold



def dateferiee(pngText):
    # On récupère la liste des dates dans le texte
    dateList = re.findall(r'([0-2]{1}[0-9]{1})[/-](1[0-2]{1}|0[1-9]{1})[/-]([0-9]{2,4})', pngText)
    dateList = list(dict.fromkeys(dateList))
    # On récupère la liste des indices sur Alsace-Moselle dans le texte
    cpList = re.findall(r'[5-6]7\d{3}', pngText)
    cityList = re.findall(r'[a|A]lsace|[m|M]oselle', pngText)

    # On initialise le résultat
    result = False

    for dateSplit in dateList :
        dateFormat = date(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0]))

        # Si la date est inférieure à la durée maximale de remboursement,        
        if relativedelta(date.today(), dateFormat).years < constants.MAX_REFUND_YEARS :

            # Si on est en Alsace-Moselle
            if len(cpList) > 0 or len(cityList) > 0 :
                if JoursFeries.is_bank_holiday(dateFormat, zone="Alsace-Moselle") :
                    result = True
                    break
            else :
                # Si c'est un jour férié en Métropole, on suspecte une fraude
                if JoursFeries.is_bank_holiday(dateFormat, zone="Métropole") :
                    result = True
                    break
    return result

def rononsoumis(pngText):
    # On récupère les indices relatifs au régime obligatoire
    regimeList = re.findall(r'[r|R][é|e]gime [o|O]bligatoire|[R|r][O|o]|REGIME OBLIGATOIRE', pngText)
    # print(regimeList)
    # On recherche les indices relatifs aux prestations non soumis au Régime obligatoire
    sansRoList = re.findall("|".join(constants.NONRO_PRESTA), pngText)

    if "" in sansRoList:
        sansRoList=[]
    
    # print(sansRoList)

    # Si l'on trouve
    if len(regimeList) > 0 and len(sansRoList) > 0 :
        return True
    else :
        return False
    

def finessfaux(pngText):
    # On récupère la liste des Numéros finess des adhérents suspects
    data = pd.read_excel(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\docker\v2\app2\surveillance.xlsx', sheet_name="finess")
    finessList = data["NUMERO FINESS"].tolist()
    print(finessList)
    print("|".join(str(s) for s in finessList))
    # On recherche les indices relatifs à la présence d'un numéro finess dans la page
    resultList = re.findall(r"|".join(str(s) for s in finessList), pngText)
    
    print(resultList)
    if len(resultList) > 0 :
        return True
    else :
         return False



def adherentssuspicieux(pngText):
    # On récupère la liste des noms des adhérents suspects
    data = pd.read_excel(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\docker\v2\app2\surveillance.xlsx', sheet_name="Adhérents")
    usersList = data["NOM Complet"].tolist()
    print(usersList)
    resultList = re.findall("|".join(usersList).upper(), pngText.upper())
    print(resultList)

    if len(resultList) > 0 :
        return True
    else :
         return False



def refarchivesfaux(pngText):
    # Recherche de mots indiquant que c'est un décompte
    rechmot = re.findall(r'CPAM|ensemble|Agir', pngText)
    
    if 'CPAM' in rechmot or 'ensemble' in rechmot or 'Agir' in rechmot:
        # On récupère la liste des références d'archivage
        refList = re.findall(r'\d{4}[ ]?[  ]?[   ]?(\d{2})(\d{3})\d{8}', pngText)
        print("Références d'archivage trouvées :", refList)

        if not refList:
            return False
        else:
            # On récupère la liste des dates dans le texte
            dateList = re.findall(r'([0-2]{1}[0-9]{1})[/-](1[0-2]{1}|0[1-9]{1})[/-]([0-9]{2,4})', pngText)
            print("Dates trouvées :", dateList)
            
            # On récupère la date de règlement
            date_reglement = re.findall(r'réglé le(?: :)? (0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/((?:\d{4}|\d{2}))(?:\sau destinataire)?', pngText)
            print("Date de règlement :", date_reglement)

            if not date_reglement:
                return False
            else:
                # Convertir la date de règlement en objet datetime
                date_reglement = date(int(date_reglement[0][2]), int(date_reglement[0][1]), int(date_reglement[0][0]))

                # Pour chaque date récupérée
                for dateSplit in dateList:
                    dateFormat = date(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0]))
                    # Comparer si une des dates de dateList est supérieure à la date de règlement
                    if dateFormat > date_reglement:
                        print("------Une date dans dateList est supérieure à la date de règlement !")
                        return True
                    else:
                        print("aucune date est superieur a la date de reglement")

                # Pour chaque référence d'archivage, on vérifie qu'il y a au moins une date qui correspond à cette référence d'archivage
                for refSplit in refList:
                    currentResult = False
                    # Pour chaque date récupérée
                    for dateSplit in dateList:
                        dateFormat = date(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0]))
                        dateCompare = date(int(dateSplit[2]), 1, 1)
                        dateDelta = dateFormat - dateCompare

                        # On vérifie que l'année correspond
                        if dateSplit[2][-2:] == refSplit[0]:
                            # On vérifie que le nombre de jours correspond
                            if int(refSplit[1]) - constants.REF_AGE_DELTA <= int(dateDelta.days) <= int(refSplit[1]) + constants.REF_AGE_DELTA:
                                currentResult = True
                                break

                    if currentResult == False:
                        print("------Une fausse référence d'archivage a été trouvée !")
                        return True

                return False
    else:
        return False

