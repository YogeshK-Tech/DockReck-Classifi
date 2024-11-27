import os
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import Dataset
import torch
import torch.nn as nn

# Path to the folder containing your text files
processed_folder = 'processed'

# Load the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Function to load the dataset from text files
def load_data(processed_folder):
    texts = []
    labels = []

    for filename in os.listdir(processed_folder):
        if filename.endswith(".txt"):
            # Extract category and subcategory from filename
            category, subcategory = filename.rsplit('.', 1)[0].split('_')
            # Read the content of the text file with explicit encoding
            try:
                with open(os.path.join(processed_folder, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                texts.append(text)
                labels.append((category, subcategory))  # Store as tuple of category and subcategory
            except UnicodeDecodeError as e:
                print(f"Error reading {filename}: {e}")

    # Convert to a HuggingFace Dataset
    dataset = Dataset.from_dict({
        'text': texts,
        'category': [label[0] for label in labels],
        'subcategory': [label[1] for label in labels]
    })
    return dataset

# Load the dataset
dataset = load_data(processed_folder)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Prepare the model: DistilBERT for multi-output sequence classification
num_categories = len(set(dataset['category']))  # Number of unique categories
num_subcategories = len(set(dataset['subcategory']))  # Number of unique subcategories

# Custom DistilBERT model with two separate classification heads
class DistilBertMultiOutputForSequenceClassification(DistilBertForSequenceClassification):
    def __init__(self, config, num_categories, num_subcategories):
        super().__init__(config)
        self.category_classifier = nn.Linear(config.hidden_size, num_categories)
        self.subcategory_classifier = nn.Linear(config.hidden_size, num_subcategories)

    def forward(self, input_ids=None, attention_mask=None, labels=None, **kwargs):
        outputs = super().forward(input_ids=input_ids, attention_mask=attention_mask, labels=None, **kwargs)
        hidden_state = outputs[0]  # Directly use the outputs for classification (logits)

        category_logits = self.category_classifier(hidden_state[:, 0, :])  # Using [CLS] token for classification
        subcategory_logits = self.subcategory_classifier(hidden_state[:, 0, :])

        return (category_logits, subcategory_logits)

# Load the model
model = DistilBertMultiOutputForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_categories=num_categories,
    num_subcategories=num_subcategories
)

# Prepare the dataset for training
train_dataset = tokenized_datasets

# Define the loss function
def compute_loss(model, inputs, return_outputs=False):
    # Forward pass
    category_logits, subcategory_logits = model(**inputs)

    # Create labels
    category_labels = inputs.get("category")
    subcategory_labels = inputs.get("subcategory")

    # Compute loss for both outputs
    category_loss = nn.CrossEntropyLoss()(category_logits, category_labels)
    subcategory_loss = nn.CrossEntropyLoss()(subcategory_logits, subcategory_labels)

    # Combine the losses
    total_loss = category_loss + subcategory_loss
    return (total_loss, (category_logits, subcategory_logits)) if return_outputs else total_loss

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',            # output directory
    num_train_epochs=3,                # number of training epochs
    per_device_train_batch_size=8,     # batch size per device during training
    logging_dir='./logs',              # directory for storing logs
    logging_steps=10,                  # number of steps before logging
)

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
      # Specify custom loss function
)

# Train the model
trainer.train()

# Save the model and tokenizer after training
model.save_pretrained('distilbert-classifier')
tokenizer.save_pretrained('distilbert-classifier')

# Inference function using the trained model
from transformers import pipeline

# Load the trained model and tokenizer for inference
classifier = pipeline('text-classification', model='distilbert-classifier', tokenizer='distilbert-classifier')

# Example of classifying a new document
doc_text = "This is a new document that needs classification."
predictions = classifier(doc_text)

print("Predictions:", predictions)
