import os
import cv2
import numpy as np

def apply_blur_to_all(input_folder, output_folder, blur_radius=30, num_blurs=7):
    # Assurez-vous que le dossier de sortie existe
    os.makedirs(output_folder, exist_ok=True)

    # Liste des extensions d'image prises en charge
    image_extensions = ['.jpg', '.jpeg', '.png']

    # Parcourir les fichiers du dossier d'entrée
    for filename in os.listdir(input_folder):
        # Vérifier si le fichier a une extension d'image
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            # Chemin complet du fichier d'entrée
            input_path = os.path.join(input_folder, filename)

            try:
                # Charger l'image
                image = cv2.imread(input_path)

                # Vérifier si l'image a été chargée correctement
                if image is not None and image.size != 0:
                    # Générer trois positions aléatoires distinctes
                    height, width, _ = image.shape
                    random_positions = [
                        (np.random.randint(blur_radius, width - blur_radius - 1), np.random.randint(blur_radius, height - blur_radius - 1))
                        for _ in range(num_blurs)
                    ]

                    # Appliquer le flou à chaque position
                    for random_x, random_y in random_positions:
                        roi = image[random_y - blur_radius:random_y + blur_radius,
                                    random_x - blur_radius:random_x + blur_radius]
                        kernel_size = 2 * blur_radius + 1
                        roi_blurred = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
                        image[random_y - blur_radius:random_y + blur_radius,
                              random_x - blur_radius:random_x + blur_radius] = roi_blurred

                    # Chemin complet du fichier de sortie
                    output_path = os.path.join(output_folder, f'blurred_{filename}')

                    # Enregistrer l'image floutée dans le dossier de sortie
                    cv2.imwrite(output_path, image)
                    print(f"Image floutée enregistrée : {output_path}")
                else:
                    print(f"Erreur de chargement de l'image : {input_path}")

            except Exception as e:
                # Ignorer l'image et afficher l'erreur
                print(f"Erreur lors du traitement de l'image {filename}: {e}")

# Exemple d'utilisation avec un rayon de flou de 100 pixels et trois carrés de flou :
input_folder = r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\sharpv5'
output_folder = r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\blurv5'

apply_blur_to_all(input_folder, output_folder, blur_radius=100, num_blurs=7)