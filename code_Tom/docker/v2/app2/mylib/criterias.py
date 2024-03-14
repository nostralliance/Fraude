import re 
import pandas as pd
from . import constants,paths
from datetime import date
from jours_feries_france import JoursFeries
from dateutil.relativedelta import relativedelta
# from autocorrect import Speller
import cv2
import argparse
# from imutils import paths
from datetime import datetime
import numpy as np


# Définir une fenêtre de détection du flou
window_size = 9

# Définir un seuil pour l'écart-type
threshold = 100

# Seuil pour le ratio de blanc dans les carre rouges
white_ratio_threshold = 0.95

# Seuil pour le ratio de noir dans les carre rouges
black_ratio_threshold = 0.05




def detect_blur(image, threshold):
    # Calculer l'ecart-type de la luminosite des pixels
    blur_map = cv2.Laplacian(image, cv2.CV_64F).var()

    # Si l'écart-type est inferieur au seuil et compris entre 0 et 5, l'image est floue
    if 0 < blur_map < threshold and 0 < blur_map < 3:
        return True, blur_map  # Retourner également la valeur de la variance
    else:
        return False, blur_map


def red_window(image):
    # stocker les resultat de la detection de flou
    blur_results = []
    # stocker les valeurs de variance
    variance_values = []


    # Diviser l'image en fenetre et detecter le flou pour chaque fenetre
    for y in range(0, image.shape[0], window_size):
        for x in range(0, image.shape[1], window_size):
            window = image[y:y+window_size, x:x+window_size]

            is_blur, variance = detect_blur(window, threshold)
            if is_blur:
                # Vérifier le ratio de blanc et de noir dans le carré rouge
                white_ratio = np.mean(window) / 255
                black_ratio = np.mean(1 - window / 255)
                if white_ratio <= white_ratio_threshold and black_ratio >= black_ratio_threshold:
                    variance_values.append(variance)  # Stocker la valeur de la variance
                    cv2.rectangle(image, (x, y), (x+window_size, y+window_size), (0, 0, 255), 2)
                    blur_results.append(is_blur)
    
    # Retourner True si blur_results contient au moins une valeur True
    print("Rsultat de True :",blur_results)
    print("Nombre de True :", len(blur_results))
    return any(blur_results)





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
    data = pd.read_excel(r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\docker\v2\app2\surveillance.xlsx', sheet_name="finess")
    finessList = data["NUMERO FINESS"].tolist()
    # print(finessList)
    # print("|".join(str(s) for s in finessList))
    # On recherche les indices relatifs à la présence d'un numéro finess dans la page
    resultList = re.findall(r"|".join(str(s) for s in finessList), pngText)
    
    print(resultList)
    if len(resultList) > 0 :
        return True
    else :
         return False



def adherentssuspicieux(pngText):
    # On récupère la liste des noms des adhérents suspects
    data = pd.read_excel(r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\docker\v2\app2\surveillance.xlsx', sheet_name="Adhérents")
    usersList = data["NOM Complet"].tolist()
    # print(usersList)
    resultList = re.findall("|".join(usersList).upper(), pngText.upper())
    # print(resultList)

    if len(resultList) > 0 :
        return True
    else :
         return False


def compare(date_simple_str, date_reglement_str):
    # convertir objet str en datetime
    date_simple = datetime.strptime(date_simple_str, "%d/%m/%Y")
    date_reglement = datetime.strptime(date_reglement_str, "%d/%m/%Y")

    # Comparer les dates
    if date_simple > date_reglement:
        print(f"{date_simple_str} est supérieure à {date_reglement_str}")
        return True
    else:
        print(f"{date_simple_str} n'est pas supérieure à {date_reglement_str}")
        return False

def extract_reglement_date(value):
    regex_regle = r'réglé le (\d{1,2}/\d{1,2}/\d{4})'
    regex_destinataire = r'(\d{1,2}/\d{1,2}/\d{4}) au destinataire'
    regex_euro = r'(\d{1,2}/\d{1,2}/\d{4}) : (\d+(?:,\d{1,2})?) euro' # Ajouter le faite qu'il peut avoir un montant en euro
    match_regle = re.search(regex_regle, value)
    match_destinataire =re.search(regex_destinataire, value)
    match_euro = re.search(regex_euro, value)

    if match_regle:
        return match_regle.group(1)
    
    elif match_destinataire:
        return match_destinataire.group(1)
    
    elif match_euro:
        return match_euro.group(1)
    
    return None



def isDateSimple(value):
    regex_simple = r'\b(?:[0-3]?[0-9][/|-](?:1[0-2]|0?[1-9])[/|-](?:\d{2}|\d{4}))\b'
    return re.match(regex_simple, value)



def date_compare(pngText):
    myBlocs = []
    currentBloc = []
    started = False
    for value in pngText:
        if not started:
            currentBloc = []
            started = True

        if isDateSimple(value) and "au destinataire" not in value:  # Ajout de la condition ici
            currentBloc.append(value)

        reglement_date = extract_reglement_date(value)
        if reglement_date:
            currentBloc.append(reglement_date)
            myBlocs.append(currentBloc)
            currentBloc = []

    date_superieur_trouver = False
    for block in myBlocs:
        date_reglement = block[-1]
        print("date de règlement :", date_reglement)
        date_normales = block[:-1]
        print("date simple :", date_normales)

        for date in date_normales:
            result = compare(date, date_reglement)
            if result:
                date_superieur_trouver = True
                break
        if date_superieur_trouver:
            break
    return date_superieur_trouver


def count_ref(pngText):
    result = False

    for text in pngText:
        pattern = re.compile(r'r[é|ë|è]f (\d+)[ ]?[ ][ ]?[ ]?(\d+)')
        matches = pattern.findall(text)

        if matches:
            for match in matches:
                group_variable = ''.join(match)
                print("result group variable:", group_variable)

                if len(group_variable) > 17:
                    print("la reference d'archivage est superieur a 17")
                    result = True
                else:
                    print("la reference d'archivage n'est pas superieur a 17")
                    result = False

    return result



def refarchivesfaux(pngText):
    rechmot = re.findall(r'CPAM|ensemble|Agir', pngText)
    
    if 'CPAM' in rechmot or 'ensemble' in rechmot or 'Agir' in rechmot:
        refList = re.findall(r'\d{4}[ ]?[  ]?[   ]?(\d{2})(\d{3})\d{8}', pngText)
        print("Références d'archivage trouvées :", refList)

        if not refList:
            return False
        else:
            dateList = re.findall(r'([0-2]{1}[0-9]{1})[/-](1[0-2]{1}|0[1-9]{1})[/-]([0-9]{2,4})', pngText)
            print("Dates trouvées :", dateList)

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

                if not currentResult:
                    print("------Une fausse référence d'archivage a été trouvée !")
                    return True

            return False
    else:
        return False