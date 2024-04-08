import cv2
from sklearn.cluster import DBSCAN
import numpy as np

# Chemin d'accès à l'image
image_test = r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\copier-coller\image_test_copier_coller\PIERRON Tom-lou.jpg'

# Code For SIFT in python using OpenCV
def siftDetector(image):
    sift = cv2.SIFT_create()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    key_points, descriptors = sift.detectAndCompute(gray, None)

    return key_points, descriptors

def locateForgery(image, key_points, descriptors, eps=90, min_sample=4):
    clusters = DBSCAN(eps=eps, min_samples=min_sample).fit(descriptors) # Find clusters using DBSCAN
    size = np.unique(clusters.labels_).shape[0] - 1
    print("nombre de cluster trouver", size)
    forgery = image.copy()
    if (size == 0) and (np.unique(clusters.labels_)[0] == -1):
        print('No Forgery Found!!')
        return None
    if size == 0:
        size = 1
    cluster_list = [[] for i in range(size)]       # List of list to store points belonging to the same cluster
    for idx in range(len(key_points)):
        if clusters.labels_[idx] != -1:
            cluster_list[clusters.labels_[idx]].append((int(key_points[idx].pt[0]), int(key_points[idx].pt[1])))
    for points in cluster_list:
        if len(points) > 1:
            for idx1 in range(1, len(points)):
                cv2.line(forgery, points[0], points[idx1], (255, 0, 0), 5)  # Draw line between the points in a same cluster
    return forgery

# Charger l'image
image = cv2.imread(image_test)

# Vérifier si l'image est chargée avec succès
if image is None:
    print("Impossible de charger l'image.")
else:
    # Appeler la fonction siftDetector
    key_points, descriptors = siftDetector(image)
    forgery_image = locateForgery(image, key_points, descriptors)
    
    # Vérifier si l'image de contrefaçon est valide
    if forgery_image is not None and forgery_image.size > 0:
        # Afficher l'image
        cv2.imshow('Forgery Image', forgery_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Aucune image de contrefaçon trouvée.")
