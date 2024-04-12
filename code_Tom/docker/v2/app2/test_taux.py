import re

# Liste de mots
mots = ['Page 1/1', '@Assurance', 'Maladie', 'LE', '0 2', 'Agir ensemble, protéger chacun', 'assuré socal RULLIERE SIMONE', 'n? de Sécurité Sociale 244 0243 129 002 18', 'Pour toutes vos démarches; utilisez le compte ameli', 'CPAM de HAUTE-LOIRE', 'avenue André Soulier - CS 70324', "ou l'application ameli pour smartphone", '43009 LE PUY-EN-VELAY CEDEX', 'MME RULLIERE SIMONE', '52 RUE DU 11 NOVEMBRE', '43220 DUNIERES', 'Voici le détail des versements vous concemant pour la joumé du 03/01/2024', "Ces informations ont été directement transmises par votre caisse d'assurance maladie à votre organisme", 'complémentaire', "En conséquence vous n'avez pas besoin de lui envoyer ce relevé", 'pour information', 'montant', 'base du', 'montant', 'dates', 'nature dos prestations', 'payé   rembours.', 'taux', 'versé', 'pour SIMONE né(e) le 15/02/1944', 'maladie', 'r8f 7581   2400240005708', '29/12/2023', 'MONTURE OPTIQUE B', 'Mo3', '175,00', '0,07', '60 %', '0,03', '29/12/2023', 'VERRE OPTIQUE 8', '( VM2 )', '285,00', '0,05', '60 %', '0,03', '29/12/2023', 'VERRE OPTIQUE B', '( VM2', '285,00', '0,05', '60 %', '0,03', 'réglé le 03/01/2024 au destinataire JUSTUN REGARD MONSIEUR D EBARD REMI', '0,09 euro(s)', 'NF Idhexeul; N a82 604', '&   Noua', 'Jve   c', 'cua', 'Ae mhouase wéxk', 'fea']



# Expression régulière pour trouver les pourcentages
def taux_compare(pngText):
    regex = re.compile(r"\d+(?:,\d+)?[ ]?%")
    for pourcentage_index, pourcentage in enumerate(pngText):
        if re.match(regex, pourcentage):
            pourcentage = pourcentage.replace("%", "")
            print(f"Pourcentage trouvé à l'index {pourcentage_index}: {pourcentage}")
            if pourcentage_index > 0:
                mot_avant = pngText[pourcentage_index - 1].replace(",", ".")
                mot_apres = pngText[pourcentage_index + 1].replace(",", ".")
                print("Mot précédent:", mot_avant)
                print("Mot suivant:", mot_apres)
                res = float(mot_avant) * float(pourcentage) / 100
                print("le res est :",res)
                if float(res) == float(mot_apres):
                    result = False
                    print("c'est ok")
                else:
                    result = True
                    print("pas ok")

            else:
                print("Pas de mot précédent ou suivant")
    return result

print(taux_compare(mots))