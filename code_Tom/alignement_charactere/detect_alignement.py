import cv2
import easyocr
import numpy as np

def draw_boxes(image, bounds, color=(0, 255, 0), thickness=2):
    for bound in bounds:
        if len(bound) == 1:
            points = bound[0]
            if len(points) == 4:
                p0, p1, p2, p3 = points
                p0 = int(p0[0]), int(p0[1])
                p1 = int(p1[0]), int(p1[1])
                p2 = int(p2[0]), int(p2[1])
                p3 = int(p3[0]), int(p3[1])
                cv2.polylines(image, [np.array([p0, p1, p2, p3])], isClosed=True, color=color, thickness=thickness)

# Charger l'image
image_path = r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\alignement_charactere\ordo_lentille.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Détecter le texte avec EasyOCR
reader = easyocr.Reader(['fr'], gpu=False) # Remplacez 'en' par la langue souhaitée
result = reader.readtext(gray)
print(result)
# Dessiner les bounding boxes sur l'image
draw_boxes(image, [result[i][0] for i in range(len(result))])

# Afficher l'image avec les bounding boxes
cv2.imshow('Image avec bounding boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
