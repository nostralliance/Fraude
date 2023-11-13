import requests

# Chemin vers le fichier PDF que vous souhaitez téléverser
pdf_file_path = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\base64_to_pdf\essaie_facture\sample1.pdf"

# Créez un dictionnaire avec le fichier PDF en tant que fichier
files = {'pdf': open(pdf_file_path, 'rb')}

# URL de votre API Flask
url = "http://192.168.1.30:5000/upload_pdf" 

# Envoi de la requête POST avec le fichier PDF
response = requests.post(url, files=files)

# Affichage de la réponse de l'API
print(response.status_code)  # Code de statut HTTP
print(response.json())  # Réponse JSON de l'API
