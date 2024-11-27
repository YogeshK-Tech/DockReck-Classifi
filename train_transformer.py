from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from transformers import Trainer, TrainingArguments
from torch.utils.data import DataLoader, Dataset
import os
import pickle
import re
import torch


PROCESSED_FOLDER = 'processed'
MODEL_NAME = "distilbert-base-uncased"
TRAINED_MODEL_PATH = "models/transformer_model"

class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long),
        }

def preprocess_text(text):
    """
    Preprocess the text by converting to lowercase, removing special characters, etc.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

def load_documents():
    """
    Load and preprocess documents from the processed folder.
    """
    documents = []
    labels = []
    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith('.txt'):
            filepath = os.path.join(PROCESSED_FOLDER, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                documents.append(preprocess_text(text))
                
                # Attempt to predict label if the file doesn't follow the naming convention
                try:
                    label = re.split(r'\d', filename)[0].capitalize()  # Extract text before the first digit
                except IndexError:
                    print(f"Warning: Unable to extract label for {filename}. Defaulting to 'Unknown'.")
                    label = 'Unknown'
                labels.append(label)
    return documents, labels

def preprocess_texts_and_labels():
    documents, labels = load_documents()
    label_map = {label: i for i, label in enumerate(set(labels))}
    print(label_map)
    labels = [label_map[label] for label in labels]
    return documents, labels, label_map

def train_transformer():
    documents, labels, label_map = preprocess_texts_and_labels()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Split the dataset into training and evaluation sets
    train_texts, eval_texts, train_labels, eval_labels = train_test_split(
        documents, labels, test_size=0.2, random_state=42
    )

    train_dataset = TextDataset(train_texts, train_labels, tokenizer)
    eval_dataset = TextDataset(eval_texts, eval_labels, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=len(label_map)
        

    )
    

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",  # Evaluate after each epoch
        save_strategy="epoch",
        num_train_epochs=8,
        per_device_train_batch_size=8,
        logging_dir="./logs",
        logging_steps=50,
        learning_rate=6e-5,
        save_steps=100,
        
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,  # Provide the evaluation dataset
        tokenizer=tokenizer,
    )

    trainer.train()

    # Save the model and tokenizer
    os.makedirs(TRAINED_MODEL_PATH, exist_ok=True)
    model.save_pretrained(TRAINED_MODEL_PATH)
    tokenizer.save_pretrained(TRAINED_MODEL_PATH)
    with open("models/label_map.pkl", "wb") as f:
        pickle.dump(label_map, f)


if __name__ == "__main__":
    train_transformer()
