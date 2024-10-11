import fitz  # PyMuPDF
import re
import pandas as pd
from openpyxl import load_workbook

def ajout_excel(list_mail, excel_path):
    # Créer un dataframe
    df = pd.DataFrame(list_mail, columns=['Mail'])

    try:
        # Charger l'Excel existant
        book = load_workbook(excel_path)
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            writer.book = book
            # Charger le dataframe existant
            existing_df = pd.read_excel(excel_path, sheet_name='Sheet1')
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            # Écrire le dataframe combiné dans l'Excel
            combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
    except FileNotFoundError:
        # Créer un nouveau fichier si le fichier n'existe pas
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

def extract_mail(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    find_mail = re.findall(email_regex, text)
    return find_mail

def extract_text_from_pdf(pdf_path):
    # Ouvrir le fichier PDF
    document = fitz.open(pdf_path)
    
    # Extraire le texte de chaque page
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()

    return text

if __name__ == "__main__":
    pdf_path = "banque_de_france_-_-_.pdf"  # Remplacez par le chemin de votre fichier PDF
    excel_path = "emails.xlsx"  # Remplacez par le chemin de votre fichier Excel
    
    # Extraire le texte du PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Extraire les emails du texte
    list_mail = extract_mail(extracted_text)
    
    if list_mail:
        # Ajouter les emails à l'Excel
        ajout_excel(list_mail, excel_path)
        print(f"{len(list_mail)} emails ont été ajoutés à {excel_path}.")
    else:
        print("Aucun email trouvé.")
