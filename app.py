from flask import Flask, Request, request, jsonify, send_file
import os
from flask_cors import CORS
import pandas as pd
from werkzeug.utils import secure_filename
from utils import initial_dataset_creator, train_classifiers, load_model, save_model, classify_text, correct_predictions
from extract_text import extract_text_from_file
import global_config
# Google Drive Functionality Imports
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request



SCOPES = ['https://www.googleapis.com/auth/drive.file']


app = Flask(__name__)
# CORS configuration for allowing all origins during development
CORS(app, resources={r"/*": {"origins": ["http://localhost:5174"]}}, supports_credentials=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Temporary storage for classified documents
classified_docs = []

@app.route("/initial_run", methods=["POST"])
def initial_run():
    """This code will run the steps 1-2"""
    try:
        initial_dataset_creator(PROCESSED_FOLDER)  # will create labelled_sjon
        global_config.data_df = pd.read_json('labelled_json.json')
        train_classifiers()
        save_model()
        return jsonify({"Status": "Success"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

@app.route("/files/<path:filename>")
def serve_file(filename):
    try:
        return send_file(filename)
    except FileNotFoundError:
        return "File not found", 404

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No files part"}), 400

    files = request.files.getlist('file')
    if not files or all(file.filename == '' for file in files):
        return jsonify({"message": "No selected files"}), 400

    predictions = []
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # Extract text and generate embeddings
                text = extract_text_from_file(file_path)
                embedding = global_config.model.encode(text)
                if len(embedding.shape) == 1:  # Ensure embedding is 2D
                    embedding = embedding.reshape(1, -1)

                # Predict category and subcategory
                try:
                    load_model()
                except FileNotFoundError:
                    print("Models not found. Initializing fresh models.")
                    global_config.cat_classifier = None
                    global_config.subcat_classifier = None

                category, subcategory = classify_text(text)

                # Add the new classified file into the data df
                new_row = {
                    "File_Name": filename,
                    "Text": text,
                    "Category": category,
                    "Subcategory": subcategory,
                    "Embeddings": embedding.tolist()  # Convert NumPy array to list for JSON compatibility
                }
                global_config.data_df = pd.concat([global_config.data_df, pd.DataFrame([new_row])], ignore_index=True)
                predictions.append({
                    "file_name": filename,
                    "category": category,
                    "subcategory": subcategory
                })

            except Exception as e:
                errors.append({"file_name": filename, "error": str(e)})
        else:
            errors.append({"file_name": file.filename, "error": "Invalid file format"})

    response = {
        "message": "File successfully processed",
        "predictions": predictions,
        "errors": errors
    }
    print(response)
    if predictions:
        return jsonify(response), 200
    else:
        return jsonify(response), 400

@app.route('/get_classified_docs', methods=['GET'])
def get_classified_docs():
    upload_folder = app.config['UPLOAD_FOLDER']
    result_df = global_config.data_df.drop(columns=["Embeddings"], errors="ignore")

    if result_df.empty:
        return jsonify({"message": "No classified documents available."}), 200

    docs_data = []
    for _, row in result_df.iterrows():
        file_name = row["File_Name"]
        file_extension = file_name.split('.')[-1].upper()
        file_path = os.path.join(upload_folder, file_name)

        if not os.path.exists(file_path):
            continue

        docs_data.append({
            "name": file_name,
            "category": row["Category"],
            "subcategory": row["Subcategory"],
            "type": file_extension,
            "url": file_path
        })
    global classified_docs
    classified_docs = docs_data

    return jsonify({"docs": docs_data}), 200

@app.route("/update_label", methods=["POST"])
def update_label():
    """This will update label and retrain"""
    data = request.get_json()

    if 'name' not in data or 'category' not in data or 'subcategory' not in data:
        return jsonify({"message": "Missing required fields: name, category, and subcategory."}), 400
    msg = correct_predictions(data['name'], data['category'], data['subcategory'])

    response = {
        "docs": [{
            "message": msg,
            "document": data
        }]
    }

    return jsonify(response), 200


@app.route("/save_todrive", methods=["POST"])
def save_todrive():
    """This will save classified documents to Google Drive."""
    try:
        service = authenticate_google_drive()  # You'll need a function to authenticate with Google Drive
        save_files_to_drive(service, classified_docs)  # Using the function you already defined
        return jsonify({"message": "Files uploaded to Google Drive!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def authenticate_google_drive():
    """Authenticate and return a Google Drive API service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=5001)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service


# Folder creation helper
def get_or_create_folder(service, folder_name, parent_id=None):
    """Creates a folder in Google Drive or returns the ID if it exists."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = (
        service.files()
        .list(q=query, spaces="drive", fields="files(id, name)", pageSize=10)
        .execute()
    )
    items = results.get("files", [])
    if items:
        return items[0]["id"]  # Return the first matching folder ID

    # Create the folder if it doesn't exist
    file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        file_metadata["parents"] = [parent_id]

    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]

def save_files_to_drive(service, classified_docs):
    """
    Saves files from classified_docs to Google Drive.
    """
    print("called save_files_to_drive")
    try:
        successful_uploads, failed_uploads = [], []
        
        for doc in classified_docs:
            if not os.path.exists(doc['url']):
                failed_uploads.append({"name": doc['name'], "error": "File not found."})
                continue

            try:
                drive_file_id = upload_file_to_drive(
                    service,
                    doc['url'],
                    doc['category'],
                    doc['subcategory']
                )
                successful_uploads.append({"name": doc['name'], "drive_file_id": drive_file_id})
            except Exception as e:
                failed_upload = {"name": doc['name'], "error": str(e)}
                failed_uploads.append(failed_upload)
                print("Failed upload:", failed_upload)



        if successful_uploads:
            print(f"Successfully uploaded: {successful_uploads}")
        if failed_uploads:
            print(f"Failed uploads: {failed_uploads}")

    except Exception as e:
        print(f"Error during file upload to Drive: {str(e)}")


def upload_file_to_drive(service, file_path, category, subcategory):
    root_folder = get_or_create_folder(service, 'DocReck Library')
    category_folder = get_or_create_folder(service, category, root_folder)
    subcategory_folder = get_or_create_folder(service, subcategory, category_folder)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [subcategory_folder]
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

if __name__ == "__main__":
    app.run(debug=True)
