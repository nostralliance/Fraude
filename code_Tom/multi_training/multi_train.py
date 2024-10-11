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

# Configuration du chemin du dataset et des tailles d'image
DATA_DIR = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\multi_training\bdd_v1"
IMAGE_SIZE = (150, 150)

# Chemins des dossiers pour sauvegarder les modèles
MODEL_DIR = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\multi_training\models"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Préparer les générateurs d'images pour train, validation, et test
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATA_DIR, 'train'),
    target_size=IMAGE_SIZE,
    batch_size=128,
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(DATA_DIR, 'val'),
    target_size=IMAGE_SIZE,
    batch_size=128,
    class_mode='binary'
)

# Callback pour afficher le progrès de l'entraînement
class TrainingProgressCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        st.write(f"Epoch {epoch+1}/{self.params['epochs']}: Accuracy = {logs['accuracy']:.4f}, Validation Accuracy = {logs['val_accuracy']:.4f}")
    
    def on_train_end(self, logs=None):
        st.success("Entraînement terminé et modèle sauvegardé !")

# Fonction pour créer un modèle de réseau de neurones basé sur VGG16
def create_neural_network():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(*IMAGE_SIZE, 3))
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
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(*IMAGE_SIZE, 3))
    features = []
    labels = []
    max_batches = 10  # Limite le nombre de lots pour accélérer l'extraction des caractéristiques
    for i, (inputs_batch, labels_batch) in enumerate(generator):
        if i >= max_batches:
            break
        
        features_batch = base_model.predict(inputs_batch)
        features.append(features_batch)
        labels.append(labels_batch)
    features = np.concatenate(features)
    labels = np.concatenate(labels)
    features = features.reshape(features.shape[0], -1)  # Aplatir pour les modèles traditionnels
    return features, labels

# Fonction pour extraire les caractéristiques d'une seule image
def extract_single_image_features(image_array):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(*IMAGE_SIZE, 3))
    features = base_model.predict(image_array)
    features = features.reshape(features.shape[0], -1)  # Aplatir pour les modèles traditionnels
    return features

# Fonction pour entraîner les modèles et les sauvegarder
def train_selected_models(selected_models):
    model_results = {}
    
    if "Neural Network" in selected_models:
        st.write("Entraînement du réseau de neurones...")
        nn_model = create_neural_network()
        nn_model.fit(train_generator, validation_data=val_generator, epochs=3, callbacks=[TrainingProgressCallback()])
        val_acc = nn_model.evaluate(val_generator)[1]
        model_results["Neural Network"] = {"accuracy": val_acc}
        # Sauvegarder le modèle en format HDF5
        nn_model_path = os.path.join(MODEL_DIR, 'neural_network_model.h5')
        nn_model.save(nn_model_path)

    if "Random Forest" in selected_models:
        st.write("Entraînement du Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=50, random_state=42)
        X_train, y_train = extract_features_with_vgg16(train_generator)
        X_val, y_val = extract_features_with_vgg16(val_generator)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_val)
        val_acc = accuracy_score(y_val, y_pred)
        model_results["Random Forest"] = {"accuracy": val_acc}
        # Sauvegarder le modèle avec joblib
        rf_model_path = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
        joblib.dump(rf_model, rf_model_path)

    if "SVM" in selected_models:
        st.write("Entraînement du SVM...")
        svm_model = SVC(probability=True, random_state=42)
        X_train, y_train = extract_features_with_vgg16(train_generator)
        X_val, y_val = extract_features_with_vgg16(val_generator)
        svm_model.fit(X_train, y_train)
        y_pred = svm_model.predict(X_val)
        val_acc = accuracy_score(y_val, y_pred)
        model_results["SVM"] = {"accuracy": val_acc}
        # Sauvegarder le modèle avec joblib
        svm_model_path = os.path.join(MODEL_DIR, 'svm_model.pkl')
        joblib.dump(svm_model, svm_model_path)

    if "K-Nearest Neighbors" in selected_models:
        st.write("Entraînement du K-Nearest Neighbors...")
        knn_model = KNeighborsClassifier(n_neighbors=3)
        X_train, y_train = extract_features_with_vgg16(train_generator)
        X_val, y_val = extract_features_with_vgg16(val_generator)
        knn_model.fit(X_train, y_train)
        y_pred = knn_model.predict(X_val)
        val_acc = accuracy_score(y_val, y_pred)
        model_results["K-Nearest Neighbors"] = {"accuracy": val_acc}
        # Sauvegarder le modèle avec joblib
        knn_model_path = os.path.join(MODEL_DIR, 'k-nearest_neighbors_model.pkl')
        joblib.dump(knn_model, knn_model_path)

    if "GBM" in selected_models:
        st.write("Entraînement du Gradient Boosting Machine (GBM)...")
        gbm_model = GradientBoostingClassifier(n_estimators=50, random_state=42)
        X_train, y_train = extract_features_with_vgg16(train_generator)
        X_val, y_val = extract_features_with_vgg16(val_generator)
        gbm_model.fit(X_train, y_train)
        y_pred = gbm_model.predict(X_val)
        val_acc = accuracy_score(y_val, y_pred)
        model_results["GBM"] = {"accuracy": val_acc}
        # Sauvegarder le modèle avec joblib
        gbm_model_path = os.path.join(MODEL_DIR, 'gbm_model.pkl')
        joblib.dump(gbm_model, gbm_model_path)
    
    return model_results

# Fonction pour charger un modèle sauvegardé
def load_saved_model(model_name):
    if model_name == "Neural Network":
        model_path = os.path.join(MODEL_DIR, 'neural_network_model.h5')
        return load_model(model_path)
    else:
        model_path = os.path.join(MODEL_DIR, f'{model_name.lower().replace(" ", "_")}_model.pkl')
        return joblib.load(model_path)

# Streamlit App
st.title("Détection d'image modifiées")

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
    
    # Sélectionner un modèle
    selected_model_name = st.selectbox("Choisissez un modèle", model_options)
    
    # Télécharger une image
    uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "png", "jpeg"])
    
    # Bouton pour lancer la prédiction
    if st.button("Lancer Prédiction"):
        if uploaded_file is not None:
            st.write(f"Tentative de chargement du modèle: {selected_model_name}")
            try:
                selected_model = load_saved_model(selected_model_name)
                st.success(f"{selected_model_name} chargé avec succès!")
                
                # Prétraitement de l'image
                image = Image.open(uploaded_file)
                st.image(image, caption='Image chargée', use_column_width=True)
                
                img = image.resize(IMAGE_SIZE)
                img_array = np.array(img)
                
                # Vérifier les dimensions
                st.write(f"Dimensions de l'image après redimensionnement : {img_array.shape}")
                
                # Vérifier que l'image a 3 canaux (RGB)
                if img_array.ndim == 2:  # Image en niveaux de gris
                    img_array = np.stack([img_array] * 3, axis=-1)
                elif img_array.shape[2] != 3:  # Si ce n'est pas RGB
                    img_array = np.stack([img_array] * 3, axis=-1)
                
                img_array = img_array / 255.0  # Normaliser les valeurs des pixels
                
                # Ajuster la forme du tableau pour le modèle
                img_array = img_array.reshape(1, *IMAGE_SIZE, 3)
                
                # Faire la prédiction
                if selected_model_name == "Neural Network":
                    prediction = selected_model.predict(img_array)[0][0]
                    label = "modifier" if prediction > 0.5 else "non modifier"
                else:
                    features = extract_single_image_features(img_array)
                    prediction = selected_model.predict(features)[0]
                    label = "modifier" if prediction == 1 else "non modifier"
                
                st.write(f"Le modèle prédit que l'image est : **{label}**")
            except Exception as e:
                st.error(f"Erreur lors de la prédiction: {e}")
        else:
            st.error("Veuillez télécharger une image avant de faire la prédiction.")
