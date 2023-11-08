import base64
import json

# Ouvrir le fichier PDF en mode lecture binaire ('rb')
with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\essaie_facture\jeu.pdf', 'rb') as pdf:
    # Lire le contenu du fichier PDF
    pdf_content = pdf.read()

# Convertir le contenu en base64
pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

# Créer un dictionnaire JSON avec la donnée base64
data = {
    "base64": pdf_base64
}

# Écrire le dictionnaire JSON dans un fichier
with open(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\base64.json', 'w') as json_file:
    json.dump(data, json_file)

print("Données PDF converties en base64 et enregistrées dans base64.json")
