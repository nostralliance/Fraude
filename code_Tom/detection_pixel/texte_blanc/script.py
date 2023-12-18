from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf(images, output_pdf):
    # Créer un nouveau PDF
    pdf = canvas.Canvas(output_pdf, pagesize=letter)

    # Taille de la page
    page_width, page_height = letter

    # Ajouter chaque image au PDF sur une nouvelle page
    for img_path in images:
        pdf.drawInlineImage(img_path, 0, 0, width=page_width, height=page_height)
        pdf.showPage()

    # Enregistrer le PDF final
    pdf.save()

def main(input_folder, output_folder):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Liste de tous les fichiers dans le dossier d'entrée
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Diviser les images en groupes de 10
    for i in range(0, len(image_files), 10):
        # Sélectionner le groupe d'images actuel
        current_images = image_files[i:i+10]

        # Créer un nom de fichier PDF basé sur le premier et le dernier fichier du groupe
        pdf_filename = f"{current_images[0]}_to_{current_images[-1]}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)

        # Chemin complet des images dans le groupe
        full_image_paths = [os.path.join(input_folder, img) for img in current_images]

        # Créer le PDF à partir du groupe d'images actuel
        create_pdf(full_image_paths, pdf_path)

if __name__ == "__main__":
    input_folder = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\non_modifier"
    output_folder = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\pdf"
    main(input_folder, output_folder)
