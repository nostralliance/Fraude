import cv2
import os

def is_image_blurry(image_path, threshold_scale=1.0):
    # Charger l'image 
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



image_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\3(3)_page-0001.jpg'
res = is_image_blurry(image_path, threshold_scale=0.0001)
print(res)







# def main(folder_path):
#     # Parcourir tous les fichiers du dossier
#     for filename in os.listdir(folder_path):
#         if filename.endswith(('.jpg', '.jpeg', '.png')):
#             # Chemin complet de l'image
#             image_path = os.path.join(folder_path, filename)

#             # Vérifier si l'image est floue avec un seuil ajusté en fonction de la résolution
#             blurry = is_image_blurry(image_path, threshold_scale=0.0001)

#             # Afficher le résultat
#             result = "Floue" if blurry else "Nette"
#             print(f"{filename}: {result}")

# if __name__ == "__main__":
#     # Remplacez "chemin_du_dossier" par le chemin de votre dossier d'images
#     main(r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc")
