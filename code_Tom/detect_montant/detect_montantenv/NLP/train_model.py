import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Charger les données
data = pd.read_csv(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detect_montant\detect_montantenv\data.csv', sep=',')

print(f'les datas : {data}')

# Convertir les données en un format compatible avec Hugging Face
data['label'] = data['label'].astype('category').cat.codes  # Convertir les labels en codes numériques
train_texts, test_texts, train_labels, test_labels = train_test_split(data['text'].tolist(), data['label'].tolist(), test_size=0.2)

# Créer des jeux de données Hugging Face
train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
test_dataset = Dataset.from_dict({"text": test_texts, "label": test_labels})

# Charger le tokenizer et le modèle
model_name = "dbmdz/bert-base-french-europeana-cased"  # Modèle BERT pour le français
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(data['label'].unique()))

# Tokenisation des données
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

train_tokenized = train_dataset.map(tokenize_function, batched=True)
test_tokenized = test_dataset.map(tokenize_function, batched=True)

# Définir les arguments d'entraîne
# ment
training_args = TrainingArguments(
    output_dir='./results',          # dossier pour stocker les résultats
    eval_strategy="epoch",     # évaluer chaque époque
    learning_rate=2e-5,
    per_device_train_batch_size=8,   # taille du lot d'entraînement
    per_device_eval_batch_size=8,    # taille du lot d'évaluation
    num_train_epochs=3,              # nombre d'époques
    weight_decay=0.01,               # régularisation
)

# Créer un Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=test_tokenized,
)

# Entraîner le modèle
trainer.train()

# Évaluer le modèle
trainer.evaluate()

# Sauvegarder le modèle
model.save_pretrained(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detect_montant\detect_montantenv\montant_detector_model')
tokenizer.save_pretrained(r'C:\Users\pierrontl\Documents\GitHub\Fraude\code_Tom\detect_montant\detect_montantenv\montant_detector_model')
