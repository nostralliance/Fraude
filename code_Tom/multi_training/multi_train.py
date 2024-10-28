import streamlit as st
import numpy as np
import os
import joblib
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
from PIL import Image

# Configuration des chemins de répertoires et des tailles d'image
DATA_DIR = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\multi_training\bdd_v1"
MODEL_DIR = r"C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\multi_training\models"
IMAGE_SIZE = (150, 150)

os.makedirs(MODEL_DIR, exist_ok=True)

# Préparer les générateurs d'images pour train et validation
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATA_DIR, 'train'),
    target_size=IMAGE_SIZE,
    batch_size=32, 
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(DATA_DIR, 'val'),
    target_size=IMAGE_SIZE,
    batch_size=32,
    class_mode='binary'
)

# Callback pour afficher le progrès de l'entraînement
class TrainingProgressCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        st.write(f"Epoch {epoch + 1}: Accuracy = {logs['accuracy']:.4f}, Val Accuracy = {logs['val_accuracy']:.4f}")
    
    def on_train_end(self, logs=None):
        st.success("Entraînement terminé ! Modèle sauvegardé.")

# Fonction pour créer un modèle de réseau de neurones basé sur VGG16
def create_neural_network():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
    model = Sequential([
        base_model,
        Flatten(),
        Dense(256, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Fonction pour extraire les caractéristiques des images à l'aide de VGG16
def extract_features_with_vgg16(generator):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
    features = []
    labels = []

    for inputs_batch, labels_batch in generator:
        features_batch = base_model.predict(inputs_batch)
        features.append(features_batch)
        labels.append(labels_batch)

    features = np.concatenate(features)
    labels = np.concatenate(labels)
    return features.reshape(features.shape[0], -1), labels.flatten()  # Assurez-vous que labels est un tableau plat

# Fonction pour entraîner les modèles et les sauvegarder
def train_selected_models(selected_models):
    model_results = {}
    
    for model_name in selected_models:
        if model_name == "Neural Network":
            st.write("Entraînement du réseau de neurones...")
            nn_model = create_neural_network()
            nn_model.fit(train_generator, validation_data=val_generator, epochs=10, callbacks=[TrainingProgressCallback()])
            val_acc = nn_model.evaluate(val_generator)[1]
            model_results["Neural Network"] = {"accuracy": val_acc}
            nn_model.save(os.path.join(MODEL_DIR, 'neural_network_model.h5'))

        else:
            st.write(f"Entraînement de {model_name}...")
            X_train, y_train = extract_features_with_vgg16(train_generator)
            X_val, y_val = extract_features_with_vgg16(val_generator)

            if model_name == "Random Forest":
                model = RandomForestClassifier(n_estimators=50, random_state=42)
            elif model_name == "SVM":
                model = SVC(probability=True, random_state=42)
            elif model_name == "K-Nearest Neighbors":
                model = KNeighborsClassifier(n_neighbors=3)
            elif model_name == "GBM":
                model = GradientBoostingClassifier(n_estimators=50, random_state=42)
            else:
                continue  # Si le modèle n'est pas reconnu, on le saute
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            val_acc = accuracy_score(y_val, y_pred)
            model_results[model_name] = {"accuracy": val_acc}
            joblib.dump(model, os.path.join(MODEL_DIR, f'{model_name.lower().replace(" ", "_")}_model.pkl'))

    return model_results

# Fonction pour charger un modèle sauvegardé
def load_saved_model(model_name):
    if model_name == "Neural Network":
        return load_model(os.path.join(MODEL_DIR, 'neural_network_model.h5'))
    else:
        return joblib.load(os.path.join(MODEL_DIR, f'{model_name.lower().replace(" ", "_")}_model.pkl'))

# Streamlit App
st.title("Détection d'images modifiées")

# Onglet 1: Entraînement des modèles
tab1, tab2 = st.tabs(["Entraînement des Modèles", "Prédiction sur une Image"])

with tab1:
    st.header("Entraînement des Modèles")
    
    model_options = ["Neural Network", "Random Forest", "SVM", "K-Nearest Neighbors", "GBM"]
    selected_models = st.multiselect("Choisissez les modèles à entraîner", model_options)
    
    if st.button("Lancer l'entraînement"):
        if selected_models:
            with st.spinner("Entraînement des modèles..."):
                model_results = train_selected_models(selected_models)
                st.success("Entraînement terminé!")
                for model_name, result in model_results.items():
                    st.write(f"Précision du {model_name} sur le jeu de validation : {result['accuracy']:.4f}")
        else:
            st.error("Veuillez sélectionner au moins un modèle à entraîner.")

# Onglet 2: Prédiction sur une image
with tab2:
    st.header("Prédiction sur une Image")
    
    selected_model_name = st.selectbox("Choisissez un modèle", model_options)
    uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "png", "jpeg"])
    
    if st.button("Lancer Prédiction"):
        if uploaded_file is not None:
            try:
                selected_model = load_saved_model(selected_model_name)
                st.success(f"{selected_model_name} chargé avec succès!")

                # Prétraitement de l'image
                image = Image.open(uploaded_file)
                st.image(image, caption='Image chargée', use_column_width=True)
                
                img = image.resize(IMAGE_SIZE)
                img_array = np.array(img) / 255.0  # Normaliser les valeurs des pixels
                img_array = img_array.reshape(1, *IMAGE_SIZE, 3)  # Ajuster la forme pour le modèle

                # Faire la prédiction
                if selected_model_name == "Neural Network":
                    prediction = selected_model.predict(img_array)[0][0]
                    label = "modifier" if prediction > 0.5 else "non modifier"
                else:
                    # Extraire les caractéristiques à partir de l'image pour les modèles non réseaux de neurones
                    features = extract_features_with_vgg16(train_generator)[0]  # Utilisez ici le batch correct
                    prediction = selected_model.predict(features)
                    label = "modifier" if prediction[0] == 1 else "non modifier"
                
                st.write(f"Le modèle prédit que l'image est : **{label}**")
            except Exception as e:
                st.error(f"Erreur lors de la prédiction: {e}")
        else:
            st.error("Veuillez télécharger une image avant de faire la prédiction.")
