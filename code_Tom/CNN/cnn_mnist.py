import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from importlib import reload
import fidle


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#Ici on crée une profondeur a nos données car notre modèle en aura besoin pour la suite.
x_train = x_train.reshape(-1,28,28,1)
x_test = x_test.reshape(-1,28,28,1)


print("x_train :",x_train.shape) 
print("y_train :",y_train.shape)
print("x_test :",x_test.shape)
print("y_test :",y_test.shape)


#Normaliser les données
print("les donnée de base ressemble a ceci : Min={}, Max={}\n".format(x_train.min(), x_train.max()))

xmax = x_train.max()
x_train = x_train / xmax
x_test = x_test / xmax

print("les donnée une fois normalisé ressemble a ceci : Min={}, Max={}\n".format(x_train.min(), x_train.max()))

# étapes de visualisation.
# fidle.scrawler.images(x_train, y_train, [27],  x_size=5,y_size=5, colorbar=True, save_as='01-one-digit')
# fidle.scrawler.images(x_train, y_train, range(5,41), columns=12, save_as='02-many-digits')


'''
Model :

ce modèle contient 10 couches 
Couche d'entrée (Input) avec une forme de (28, 28, 1).

Couche de convolution 2D avec 8 filtres de taille (3, 3) et une fonction d'activation ReLU.

Couche de pooling (MaxPooling2D) avec une fenêtre de (2, 2).

Couche de dropout avec un taux de 0.2 pour la régularisation.

Couche de convolution 2D avec 16 filtres de taille (3, 3) et une fonction d'activation ReLU.

Couche de pooling (MaxPooling2D) avec une fenêtre de (2, 2).

Couche de dropout avec un taux de 0.2 pour la régularisation.

Couche d'aplatissement (Flatten) pour transformer les données en un vecteur 1D.

Couche dense avec 100 neurones et une fonction d'activation ReLU.

Couche de dropout avec un taux de 0.5 pour la régularisation.

Couche dense de sortie avec 10 neurones (correspondant aux classes de sortie) et une fonction d'activation softmax pour la classification.
'''



model = keras.models.Sequential()

model.add( keras.layers.Input(( 28 , 28 , 1 )) )

model.add( keras.layers.Conv2D( 8 , ( 3 , 3 ), activation= 'relu' ) ) # 8 ici correspond aux filtres, chaques filtres détecte des caractéristiques spécifique comme bordure textures ... detaille 3x3 pixel avec une fonction d'activation relu 
model.add( keras.layers.MaxPooling2D(( 2 , 2 )))# le max pooling lui réduit la résolution spatiale avec un kernel de 2x2 et ne prend que la plus grande valeurs des régions balayé
model.add( keras.layers.Dropout( 0.2 ))# a chaque étape d'entrainement le dropout sert a désactiver certain neurones pour éviter le surentrainement.

model.add( keras.layers.Conv2D( 16 , ( 3 , 3 ), activation= 'relu' ) )
model.add( keras.layers.MaxPooling2D(( 2 , 2 )))
model.add( keras.layers.Dropout( 0.2 ))

model.add( keras.layers.Conv2D( 32 , ( 3 , 3 ), activation= 'relu' ) )
model.add( keras.layers.MaxPooling2D(( 2 , 2 )))
model.add( keras.layers.Dropout( 0.2 ))

model.add( keras.layers.Flatten())
model.add( keras.layers.Dense( 200 , activation= 'relu' ))
model.add( keras.layers.Dropout( 0.5 ))

model.add( keras.layers.Dense( 10 , activation= 'softmax' ))

#permet de faire un sommaire du modèle 
model.summary() 

#permet de compilé les différents paramètres crée précedement
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


batch_size  = 512
epochs      =  32

#le .fit permet d'appliquer l'entrainement sur les données x_train les donnée et y_train les étiquettes associé a chaque data
history = model.fit(  x_train, y_train,
                      batch_size      = batch_size,#le lot de donnée d'entrainement
                      epochs          = epochs, #combien de fois le modèle va parcourir les donnée d'entrainement 
                      verbose         = 1,
                      validation_data = (x_test, y_test))#permet d'evaluer la performence du modèle


score = model.evaluate(x_test, y_test, verbose=0)

print(f'Test loss     : {score[0]:4.4f}')
print(f'Test accuracy : {score[1]:4.4f}')

fidle.scrawler.history(history, figsize=(6,4), save_as='03-history')

y_sigmoid = model.predict(x_test)
y_pred    = np.argmax(y_sigmoid, axis=-1)

fidle.scrawler.images(x_test, y_test, range(0,200), columns=12, x_size=1, y_size=1, y_pred=y_pred, save_as='04-predictions')