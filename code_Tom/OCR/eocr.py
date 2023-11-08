import easyocr
import cv2
import matplotlib.pyplot as plt

dict_texte = {}

image_path = r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\OCR\essaie_2.png'

# Objet easyOCR en Francais
reader = easyocr.Reader(['fr'])

# On charge l'image voulu soit essaie_2.png
image = cv2.imread(image_path)

# easyOCR ici est utiliser pour lire l'image donnée
results = reader.readtext(image)

# Dessinez les bounding boxes autour de chaque mot trouvé
for (bbox, text, prob) in results:
    dict_texte[text] = prob
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Dessinez un rectangle autour du mot
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    # cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Affichez l'image avec les bounding boxes
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
print(dict_texte)





