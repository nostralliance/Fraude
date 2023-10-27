import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import datetime
# from tensorflow import keras
# from tensorflow.keras.models import Model
# import tensorflow as tf



path_facture_vraie = r'C:/Users/pierrontl/Documents/code_python/essaie_2.png'
image_fature_vraie = cv2.imread(path_facture_vraie, cv2.IMREAD_COLOR)
plt.axis('off')
plt.imshow(cv2.cvtColor(image_fature_vraie, cv2.COLOR_BGR2RGB))
plt.show()




path_facture_fausse = r'C:/Users/pierrontl/Documents/code_python/essaie_1.png'
image_fature_fausse = cv2.imread(path_facture_fausse, cv2.IMREAD_COLOR)
plt.axis('off')
plt.imshow(cv2.cvtColor(image_fature_fausse, cv2.COLOR_BGR2RGB))
plt.show()




