from flask import Flask, redirect, request, jsonify, send_file, session, url_for
from google.auth.transport.requests import Request as GoogleAuthRequest
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from flask_session import Session
from flask_cors import CORS
import os
import pandas as pd
from werkzeug.utils import secure_filename
from flask_dance.contrib.google import make_google_blueprint, google
from utils import initial_dataset_creator, train_classifiers, load_model, save_model, classify_text, correct_predictions
from extract_text import extract_text_from_file
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from classify import classifier, classify_document
from librarymodule import SCOPES, save_files_to_drive, upload_file_to_drive, get_or_create_folder
import global_config

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set a secret key
app.secret_key = os.urandom(24)  # Generates a random 24-byte key

# CORS configuration for allowing all origins during development
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Temporary storage for classified documents (replace with a database)
classified_docs = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Google OAuth Blueprint
# google_bp = make_google_blueprint(
#     client_id="96146810234-ibpncsnk05a84n8r4off6ac3g3a5qc1l.apps.googleusercontent.com",
#     client_secret="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",
#     scope=[
#         "https://www.googleapis.com/auth/drive",          # For Google Drive access
#         "https://www.googleapis.com/auth/userinfo.email",  # For email access
#         "https://www.googleapis.com/auth/userinfo.profile" # For profile information access
#     ],
#     redirect_to="home"
# )
# app.register_blueprint(google_bp, url_prefix="/login")

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/drive',
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
]


# @app.route("/home")
# def home():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     return jsonify({"message": "Successfully authenticated with Google!"})


# @app.route('/start_oauth', methods=['GET'])
# def start_oauth():
#     # Generate the authorization URL
#     authorization_url, state = google.authorization_url(
#         'https://accounts.google.com/o/oauth2/auth'
#     )
    
#     print("Authorization URL: ", authorization_url)  # Debugging the generated URL
#     return redirect(authorization_url)

@app.route("/initial_run", methods=["POST"])
def initial_run():
    """This code will run the steps 1-2"""
    try:
        initial_dataset_creator(PROCESSED_FOLDER) # will create labelled_sjon
        global_config.data_df = pd.read_json('labelled_json.json')
        train_classifiers()
        save_model()
        return jsonify({"Status": "Success"}), 200
    except Exception as e:
        return jsonify({"Error": e}), 400
    

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
            # print(f"File not found: {file_path}")
            continue

        docs_data.append({
            "name": file_name,
            "category": row["Category"],
            "subcategory": row["Subcategory"],
            "type": file_extension,
            "url": file_path
        })
    global classified_docs

    classified_docs=docs_data

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
    # Fetch user ID from the stored session cookie
    user_email = request.cookies.get('user_email')
    print("User Email:", user_email)
    if not user_email:  # Check if user_id exists in cookies
        
        return jsonify({
            "message": "User not authenticated. Redirecting to authorization.",
            "redirect_url": url_for('authorize', _external=True)
        }), 401
    
    user_id = user_email.replace('@', '_').replace('.', '_')
    
    print("User ID:", user_id)

    token_path = f'tokens/{user_id}_token.json'
    
    # Ensure the user has a valid token file
    if not os.path.exists(token_path):
        return jsonify({
            "message": "Not valid token. Redirecting to authorization.",
            "redirect_url": url_for('authorize', _external=True)
        }), 402

    # Load credentials from the token file
    credentials = Credentials.from_authorized_user_file(token_path, SCOPES)


    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(GoogleAuthRequest())
            print("Credentials refreshed successfully.")
        else:
            return jsonify({
                "message": "User not authenticated. Redirecting to authorization.",
                "redirect_url": url_for('authorize', _external=True)
            }), 404

    # Fetch the user's email as the unique identifier
    service = build('people', 'v1', credentials=credentials)
    profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
    user_email = profile['emailAddresses'][0]['value']
    print("SERVICE:",service)

    
    # Process file uploads
    try:
        successful_uploads, failed_uploads = [], []
        print("these are classified_docs:",classified_docs)
        # Assuming 'classified_docs' exists and contains document information
        # trying to create a dummy folder
        print(" called create folder")
        get_or_create_folder(service, 'DocReck Library Test 1')
        for doc in classified_docs:
            if not os.path.exists(doc['url']):
                failed_uploads.append({"name": doc['name'], "error": "File not found."})
                continue

            try:
                drive_file_id = upload_file_to_drive(service, doc['url'], doc['category'], doc['subcategory'])
                successful_uploads.append({"name": doc['name'], "drive_file_id": drive_file_id})
            except Exception as e:
                print(f"Error during file upload to Drive: {str(e)}")
                failed_uploads.append({"name": doc['name'], "error": str(e)})

        if successful_uploads:
            print(f"Successfully uploaded: {successful_uploads}")
            return jsonify({"successful_uploads": successful_uploads, "failed_uploads": failed_uploads}), 200
        else:
            print(f"No successful uploads.")
            return jsonify({"message": "No successful uploads.", "failed_uploads": failed_uploads}), 500

    except Exception as e:
        print(f"Error during file upload to Drive: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500




@app.route('/authorize')
def authorize():
    """
    Redirects the user to Google's OAuth 2.0 consent screen with the required scopes.
    """
    try:
        # Creating the OAuth flow with requested scopes
        flow = Flow.from_client_secrets_file('credentials.json', SCOPES)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        
        # Force re-consent by including the 'prompt' parameter
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')

        return redirect(auth_url)
    except Exception as e:
        return jsonify({"message": f"Error initiating authorization: {str(e)}"}), 500


@app.route('/oauth2callback')
def oauth2callback():
    """
    Handles the OAuth callback, stores user credentials, and redirects to the frontend classification screen.
    """
    try:
        # Create OAuth flow and fetch token
        flow = Flow.from_client_secrets_file('credentials.json', SCOPES)
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        flow.fetch_token(authorization_response=request.url)

        # Obtain credentials and fetch the user's email
        credentials = flow.credentials
        service = build('people', 'v1', credentials=credentials)
        profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
        user_email = profile['emailAddresses'][0]['value']

        # Save credentials to a file
        user_id = user_email.replace('@', '_').replace('.', '_')
        token_path = f'tokens/{user_id}_token.json'
        os.makedirs('tokens', exist_ok=True)
        with open(token_path, 'w') as token_file:
            token_file.write(credentials.to_json())

        # Save files to Google Drive
         # Custom function to handle the saving logic

        # Redirect to the frontend classification screen
        frontend_url = "http://localhost:5173/classification"
        response = redirect(frontend_url)
        print("user email",user_email)
        response.set_cookie("user_email" ,user_email, httponly=True, secure=False, max_age=60 * 60 * 24 * 365)
          # Cookie valid for 1 year
        email = request.cookies.get('user_email')
        print("cookie",email)
        # save_files_to_drive(service,classified_docs) 
        save_todrive()
        return response

    except Exception as e:
        return jsonify({"message": f"Error during OAuth callback: {str(e)}"}), 500





if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
