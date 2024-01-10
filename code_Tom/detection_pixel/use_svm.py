import pickle
import cv2
import numpy as np
from skimage.filters import laplace, sobel, roberts

def extract_features(image_path):
    image = cv2.imread(image_path)
    
    # Convertir l'image en niveaux de gris
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if image_gray is not None:
        lap_feat = laplace(image_gray)
        sob_feat = sobel(image_gray)
        rob_feat = roberts(image_gray)

        # Calculer les caractéristiques sur chaque canal de couleur
        lap_feat_color = np.mean([laplace(image[:, :, i]) for i in range(3)], axis=0)
        sob_feat_color = np.mean([sobel(image[:, :, i]) for i in range(3)], axis=0)
        rob_feat_color = np.mean([roberts(image[:, :, i]) for i in range(3)], axis=0)

        # Vérifier si les fonctionnalités ne sont pas None avant d'extraire les statistiques
        if lap_feat is not None and sob_feat is not None and rob_feat is not None:
            features = [lap_feat_color.mean(), lap_feat_color.var(), np.amax(lap_feat_color),
                        sob_feat_color.mean(), sob_feat_color.var(), np.max(sob_feat_color),
                        rob_feat_color.mean(), rob_feat_color.var(), np.max(rob_feat_color)]

            return np.array(features)

    return None


def classify_image(image_path, model_path):
    # Charger le modèle avec pickle
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)

    # Extraire les caractéristiques de l'image
    image_features = extract_features(image_path)

    if image_features is not None:
        # Effectuer une prédiction avec le modèle chargé
        prediction = loaded_model.predict([image_features])

        if prediction == 1:
            return "Image is sharp."
        else:
            return "Image is blurred."
    else:
        return "Unable to extract features from the image."

# Exemple d'utilisation
image_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\3.jpg'
model_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\model_vgg\final_svm.pkl'

result = classify_image(image_path, model_path)
print(result)

#modifier a certain endroits le flou pas toutes la page 