import cv2
import numpy as np

# Charger l'image
image = cv2.imread(r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\data_facture\sharpv5\SKM_30824010311110-02.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Définir une fenêtre de détection du flou
window_size = 16

# Définir un seuil pour l'écart-type
threshold = 10

# Seuil pour le ratio de blanc dans les carre rouges
white_ratio_threshold = 0.95

# Seuil pour le ratio de noir dans les carre rouges
black_ratio_threshold = 0.05

# stocker les resultat de la detection de flou
blur_results = []

# stocker les valeurs de variance
variance_values = []

# stocker la valeur des pixels 
pixels_values = []


def detect_blur(image, threshold):
    # Calculer l'ecart-type de la luminosite des pixels
    blur_map = cv2.Laplacian(image, cv2.CV_64F).var()

    # Si l'écart-type est inferieur au seuil et compris entre 0 et 5, le carré est floue
    if 0 < blur_map < threshold and 0 < blur_map < 3:
        return True, blur_map  # Retourner également la valeur de la variance
    else:
        return False, blur_map



def red_window(image):
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
                    variance_values.append(variance)  # stocker la valeur de la variance
                    pixels_values.append(window)  # stocker les valeurs de pixel
                    cv2.rectangle(image, (x, y), (x+window_size, y+window_size), (0, 255, 0), 1)
                    blur_results.append(is_blur)

    # Retourner True si blur_results contient au moins une valeur True
    print("Rsultat de True :",blur_results)
    print("Nombre de True :", len(blur_results))
    print("la valeurs des pixels de chaque carre :", pixels_values)
    return any(blur_results)

is_blur = red_window(image)

print(is_blur)

# Redimensionner l'image
height, width = image.shape[:2]
max_dim = max(height, width)
scale = 1500 / max_dim
image_resized = cv2.resize(image, None, fx=scale, fy=scale)

# Afficher l'image 
cv2.imshow("Blurred Regions", image_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Afficher les résultats 
print("Variance pour chaque fenêtre où le flou est détecté :", variance_values)