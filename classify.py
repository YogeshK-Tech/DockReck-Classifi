import os
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from datasets import Dataset
import torch
from torch.utils.data import DataLoader

# Define paths
PROCESSED_FOLDER = 'processed'

# Load pre-trained model and tokenizer from Hugging Face
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

# Create a classifier variable that can be imported
classifier = model

# Load training data
def load_training_data():
    data = []
    labels = []
    
    # Create a dictionary to map labels to numerical indices
    label_map = {}

    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith('.txt'):
            category, subcategory = filename.replace('.txt', '').split('_')
            file_path = os.path.join(PROCESSED_FOLDER, filename)

            # Read content from file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # Generate label (category_subcategory) and add to data
            label = f"{category}_{subcategory}"
            data.append(content)

            # Add to label_map if not already present
            if label not in label_map:
                label_map[label] = len(label_map)

            labels.append(label_map[label])
    
    return data, labels, label_map

# Prepare the dataset for training
def prepare_data_for_training(data, labels):
    dataset = Dataset.from_dict({'text': data, 'label': labels})
    return dataset

# Tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=512)

# Classify a single document (used in the Flask app)
def classify_document(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    
    # Move model and input to GPU if available (optional)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    classifier.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Make prediction
    with torch.no_grad():
        outputs = classifier(**inputs)
    
    # Get the predicted class index
    prediction_idx = outputs.logits.argmax(dim=-1).item()

    # Map the predicted index to category and subcategory
    data, labels, label_map = load_training_data()  # re-load to access label_map
    reversed_label_map = {v: k for k, v in label_map.items()}
    predicted_label = reversed_label_map[prediction_idx]
    category, subcategory = predicted_label.split("_")
    
    return category, subcategory

# Train the model (if necessary)
def train_model():
    data, labels, label_map = load_training_data()
    dataset = prepare_data_for_training(data, labels)
    
    # Number of unique labels
    num_labels = len(label_map)

    # Initialize the model with the correct number of labels
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_labels)

    # Split the data into training and validation sets
    train_dataset, val_dataset = dataset.train_test_split(test_size=0.1).values()

    # Apply tokenization
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    val_dataset = val_dataset.map(tokenize_function, batched=True)

    # Set format for PyTorch
    train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    # Initialize Trainer
    from transformers import Trainer, TrainingArguments

    training_args = TrainingArguments(
        output_dir='./results',          # output directory
        evaluation_strategy="epoch",     # evaluation strategy to adopt during training
        learning_rate=2e-5,              # learning rate
        per_device_train_batch_size=16,  # batch size for training
        per_device_eval_batch_size=64,   # batch size for evaluation
        num_train_epochs=3,              # number of training epochs
        weight_decay=0.01,               # strength of weight decay
    )

    trainer = Trainer(
        model=model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=val_dataset             # evaluation dataset
    )

    # Train the model
    trainer.train()

if __name__ == "__main__":
    train_model()
