import re
from price_parser import Price

# Texte d'exemple
test = "Bonjour je suis un texte et le but est repérer dans le texte des montant comme 34,46€ ou encore 27.34€ mais le problème c'est est-ce que il détecte les nombre entier genre 3456€ et 50$"

def extract_prices(text):
    # Utiliser une expression régulière pour trouver les montants dans le texte
    # Modification pour capturer les montants entiers, avec et sans espaces
    pattern = r'\b\d{1,3}(?:[\s,]\d{3})*(?:[.,]\d{2})?\s?€|\b\d+(?:[\s,]\d{3})*\s?[€|$]'
    matches = re.findall(pattern, text)

    # Affichage des montants trouvés
    print("Montants trouvés :", matches)

    prices = []
    for match in matches:
        # Nettoyer le montant en enlevant les espaces avant l'euro
        clean_match = match.replace(' ', '').strip()
        # Analyser le montant avec price-parser
        price = Price.fromstring(clean_match)
        if price.amount is not None:  # Vérifier si le montant a été correctement analysé
            prices.append(price)
    
    return prices

# Exécution de la fonction
detected_prices = extract_prices(test)

# Afficher les résultats
if detected_prices:
    for price in detected_prices:
        print(f"Montant : {price} | Valeur : {price.amount} {price.currency}")
else:
    print("Aucun montant détecté.")
