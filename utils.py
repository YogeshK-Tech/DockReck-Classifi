import os
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sentence_transformers import SentenceTransformer
import global_config


# Utility functions
def initial_dataset_creator(folder_path):
    """This is to create the json of the files in the folder"""

    labelled_json = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            file_path = os.path.join(folder_path, file)
            if "_" in file:
                file_category = file.split("_")[0]
                file_name = file.split("_", 1)[1]
                if "_" in file_name:
                    file_sub = file_name.split("_")[1].rsplit(".", 1)[0]
                else:
                    file_sub = file_name.rsplit(".", 1)[0]
            else:
                file_category = "unknown"
                file_sub = "unknown"
            with open(file_path, "r", encoding="utf-8") as f:
                file_text = f.read()

            # embeddings = global_config.model.encode(file_text)
            # if hasattr(embeddings, "tolist"):
            #     embeddings = embeddings.tolist()
            labelled_json.append({
                "File_Name": file,
                "Text": file_text,
                "Category": file_category,
                "Subcategory": file_sub,
                # "Embeddings": embeddings
            })
    output_path = os.path.join("labelled_json.json")
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(labelled_json, json_file, indent=4)

    print(f"DOne")



def train_classifiers():
    """Train classifiers for categories and subcategories."""
    df = global_config.data_df
    if df.empty:
        raise ValueError("Dataframe is empty. Cannot train classifiers.")

    # Create embeddings for all texts
    df['Embeddings'] = df['Text'].apply(lambda text: global_config.model.encode(text).tolist())
    embeddings = np.vstack(df['Embeddings'].values)
    categories = df['Category']
    subcategories = df['Subcategory']

    # Train category classifier
    X_train, X_test, y_train, y_test = train_test_split(embeddings, categories, test_size=0.2, random_state=42)
    cat_classifier = LogisticRegression()
    cat_classifier.fit(X_train, y_train)
    y_pred = cat_classifier.predict(X_test)
    print(f"Category Classifier Accuracy: {accuracy_score(y_test, y_pred)}")
    global_config.cat_classifier = cat_classifier

    # Train subcategory classifier
    X_train, X_test, y_train, y_test = train_test_split(embeddings, subcategories, test_size=0.2, random_state=42)
    subcat_classifier = LogisticRegression()
    subcat_classifier.fit(X_train, y_train)
    y_pred = subcat_classifier.predict(X_test)
    print(f"Subcategory Classifier Accuracy: {accuracy_score(y_test, y_pred)}")
    global_config.subcat_classifier = subcat_classifier


def save_model():
    """Save trained models to disk."""
    if global_config.cat_classifier:
        joblib.dump(global_config.cat_classifier, "category_classifier.pkl")
    if global_config.subcat_classifier:
        joblib.dump(global_config.subcat_classifier, "subcategory_classifier.pkl")
    print("Models saved successfully.")


def load_model():
    """Load models from disk."""
    if os.path.exists("category_classifier.pkl"):
        global_config.cat_classifier = joblib.load("category_classifier.pkl")
    if os.path.exists("subcategory_classifier.pkl"):
        global_config.subcat_classifier = joblib.load("subcategory_classifier.pkl")
    print("Models loaded successfully.")


def classify_text(text):
    """Classify text into category and subcategory."""
    if global_config.cat_classifier is None or global_config.subcat_classifier is None:
        raise ValueError("Classifiers are not loaded.")

    embedding = global_config.model.encode(text).reshape(1, -1)
    category = global_config.cat_classifier.predict(embedding)[0]
    subcategory = global_config.subcat_classifier.predict(embedding)[0]
    return category, subcategory


def extract_text_from_file(file_path):
    """Extract text from a file."""
    with open(file_path, 'r') as f:
        return f.read()


def correct_predictions(file_name, new_category, new_subcategory):
    """Update a document's labels and retrain the classifiers."""
    df = global_config.data_df
    if file_name not in df['File_Name'].values:
        return "File not found in the dataset."

    global_config.data_df.loc[df['File_Name'] == file_name, ['Category', 'Subcategory']] = [new_category, new_subcategory]
    train_classifiers()
    save_model()
    return f"Labels for {file_name} updated and classifiers retrained."
