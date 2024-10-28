from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Charger le modèle et le tokenizer sauvegardés
model = AutoModelForSequenceClassification.from_pretrained('./montant_detector_model')
tokenizer = AutoTokenizer.from_pretrained('./montant_detector_model')

def predict_montant(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_class = np.argmax(logits.numpy(), axis=1)
        return predicted_class[0]  # Renvoie le premier élément du tableau
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    text_example = "Le montant de 300 euros est à payer."
    predicted_label = predict_montant(text_example)

    # Ajoutez des étiquettes pour interpréter la sortie
    label_mapping = {0: "montant", 1: "autre"}  # Mettez à jour si nécessaire
    print(f"Label prédit : {label_mapping.get(predicted_label, 'Inconnu')}")
