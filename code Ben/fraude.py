import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from tensorflow_hub.keras_layer import KerasLayer
import pathlib
import os
from PIL import Image
import pickle
#import sklearn

#import yaml








IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_DEPTH = 3







def load_image(path):
    """Load an image as numpy array
    """
   # path = pathlib.Path('C:/Users/nathanael/Documents/Plane-classification/')
    return plt.imread(path)
    

    

@st.cache(ttl = 12*3600, allow_output_mutation=True, max_entries=5)
def predict_image(Path_class,path, model):
    """Predict plane identification from image.
    
    Parameters
    ----------
    path (Path): path to image to identify
    model (keras.models): Keras model to be used for prediction
    
    Returns
    -------
    Predicted class
    """
    
    names= pd.read_csv(Path_class,names=['Names'])
    #A=np.array(Image.open(path))
    #r, g, b = image_rgb.getpixel((w, h))
    image= [np.array(Image.open(path).convert('RGB').resize((IMAGE_WIDTH, IMAGE_HEIGHT)))]
    #print(image)
    prediction_vector = model.predict(np.array(image))
    #print(prediction_vector)
    predicted_classes = np.argmax(prediction_vector, axis=1)[0]
    names_classes=names['Names'][predicted_classes]
    #print(names)
    #print(predicted_classes)
    return prediction_vector, predicted_classes,names_classes

def load_model(path):
    """Load tf/Keras model for prediction
    """
    return tf.keras.models.load_model(path)



#bouton_ra = st.sidebar.radio(
    # "Type of model",
    # ('Reseaux de neurones', 'SVM', 'Transfert_learning'))
   
# sidebar_model =  st.sidebar.selectbox(
                  #  'Target!',
                   #  ('Manufacturer', 'Family'))






st.title("Détection de facture ")

uploaded_file = st.file_uploader("Télécharge une facture") #, accept_multiple_files=True)#



if uploaded_file:
    loaded_image = load_image(uploaded_file)
    st.image(loaded_image)
    
    
predict_btn = st.button("Identify", disabled=(uploaded_file is None))

if predict_btn :
    Path_class = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code Ben\classe_name.txt"
    #mod = 'Libellé.h5'
    mod = os.path.join('home', os.path.sep, 'Libellé.h5')
    #print(mod)
    #model = tf.saved_model.load("/Libellé.h5")
    model = load_model(r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code Ben\model_ame.h5")
    model.summary()
    #image= [np.array(Image.open(path)
    #print(loaded_image.shape)
    #image= [Image.open(uploaded_file)]
    #print(image.shape())
    prediction_vector,prediction,classes = predict_image(Path_class,uploaded_file, model)
    #prediction='ben'
    st.title("Classe")
    st.write(f"c'est une : {classes}")
    #st.title("Prédiction")
    #st.write(f"of Class number : {prediction}")
    st.title("Probabilité")
    st.write(f"Avec une probabilité de: {'{}.%'.format(prediction_vector.max()*100)}")
    st.title("Barchat")
    st.bar_chart(prediction_vector)
    
    
    


else: print('Change the model')
    
