import pathlib

#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import seaborn as sns
import tensorflow as tf

from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
import datetime
from sklearn.metrics import confusion_matrix,accuracy_score
import seaborn as sns

# from tensorflow.keras import layers

from PIL import Image



IMAGE_WIDTH = 128
IMAGE_HEIGHT = IMAGE_WIDTH
IMAGE_DEPTH = 3

# allow to build our image database
def build_image_database(path, target):
    """Build a pandas dataframe with target class and access path to images.
   
    Parameters
    - - - - - -
    path (Path): path patern to read csv file containing images information.
    target (str): name of the target column.
   
    Returns
    - - - - -
    A pandas dataframe, including target class and path to image.
    """
   
   
    _df = pd.read_csv(path, sep=';', dtype={'all': str})

   
    _df['path'] = _df['id'].apply(lambda x:  pathlib.Path(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\texte_blanc_fondblanc\facture') / (str(x) + '.png'))

    return _df

def load_resize_image(path,height,width):
  """Load an image and resize it to the target size
    Parameters
    --------
    path(Path): access path to image file
    height(int): resize image to this height
    width(int):resize image to this width

    Returns
    ----------
    nb.array containing resize



  """
  
  return np.array(Image.open(path).convert('RGB').resize((width, height)))






def build_classification_model(df:pd.DataFrame, target:str, images:str):

    nb_classes=df[target].nunique() # compute number of classees for output layer
    size = df[images].iloc[0].shape # com
    #Building the model
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu', input_shape=(128,128,3)))
    model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(2, activation='softmax'))# couche de sortie à nb_classes

    # #Compilation of the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


def build_x_and_y(df:pd.DataFrame,target:str,images:str,stratify=None):
  """Build x tensor and y tensor for model fitting 

  Parameters
  --------------
  df(pd.DataFrame):dataframe contanining images and target
  target(str):name of target column
  images(str): name of images column
  
  Returns
  ---------
  x(np.array):tensor of x values
  y(np.array):name of y values
  """
  x=np.array(df[images].to_list())
  y= tf.keras.utils.to_categorical(df[target].astype('category').cat.codes)



  return x, y



# Load train & test dataset
train_df= build_image_database(pathlib.Path(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\data_train.csv'),'label')
test_df= build_image_database(pathlib.Path(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\data_test.csv'),'label')

train_df['resized_image']=train_df.apply(lambda r:load_resize_image(r['path'],IMAGE_HEIGHT,IMAGE_WIDTH),axis=1)

test_df['resized_image']=test_df.apply(lambda r:load_resize_image(r['path'],IMAGE_HEIGHT,IMAGE_WIDTH),axis=1)
#train_df
# Build tensors for training & testing

X_train,y_train =build_x_and_y(train_df,'label','resized_image')
X_test,y_test =build_x_and_y(test_df,'label','resized_image')

# BUILD TF classification model
model = build_classification_model(train_df,'label','resized_image')

model= build_classification_model(train_df, 'label', 'resized_image')

model.summary()

epochs = 2
history = model.fit(X_train, y_train, batch_size=96, epochs=epochs, 
                    validation_data=(X_test, y_test)
                    #callbacks=[tensorboard_callback]
                    )


def classify_images(images, model, classes_names=None):
  """Classify images through a TF model.
  Parameters
  ----------
  images (np.array): set of images to classify
  model (tf.keras.Model): TF/ Keras model
  classes_names: dictionnary with classes names
  Returns
  -------
  predicted classes
  """

  results = model.predict(images) # predict for images
  classes = np.argmax(results, axis=1) # np.argmax returns the index of the max value per row
  if classes_names is not None:
    classes = np.array(classes_names[classes])
  return classes


def save_model(model, basename):
  """Save tf/Keras model

  Model file is named model + timestamp.

  Parameters
  ----------
  model (tf/Keras model): model to be saved
  basename: location to save model file
  """
  model.save('{}.h5'.format(basename))
  return

  # apply the function save_model()
save_model(model, pathlib.Path(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detection_pixel\texte_blanc\model'))


cm = confusion_matrix(np.argmax(y_train, axis=1),
                        classify_images(X_train, model))
print(cm)
cm=pd.DataFrame(cm)
# print(sns.heatmap(cm, annot=True))

ac = accuracy_score(np.argmax(y_train, axis=1),
                        classify_images(X_train, model))
print(ac)