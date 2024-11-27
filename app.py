from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from extract_text import extract_text_from_file
from classify import classifier, classify_document  # Import the classifier

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Temporary storage for classified documents (replace with a database)
classified_docs = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Extract text from file
            text = extract_text_from_file(file_path)

            # Classify using DistilBERT
            category, subcategory = classify_document(text)

            # Add to temporary storage
            classified_docs.append({
                "name": filename,
                "type": file.filename.split('.')[-1].upper(),
                "category": category,
                "subcategory": subcategory
            })

            return jsonify({
                "message": "File successfully processed and classified.",
                "predictions": {
                    "category": category,
                    "subcategory": subcategory
                }
            }), 200
        except Exception as e:
            return jsonify({"message": f"Error processing file: {str(e)}"}), 500

    return jsonify({"message": "Invalid file format."}), 400

@app.route("/get_classified_docs", methods=["GET"])
def get_classified_docs():
    return jsonify({"docs": classified_docs}), 200

@app.route("/update_label", methods=["POST"])
def update_label():
    data = request.get_json()

    if 'name' not in data or 'category' not in data or 'subcategory' not in data:
        return jsonify({"message": "Missing required fields: name, category, and subcategory."}), 400

    doc = next((doc for doc in classified_docs if doc['name'] == data['name']), None)

    if not doc:
        return jsonify({"message": "Document not found."}), 404

    doc['category'] = data['category']
    doc['subcategory'] = data['subcategory']

    return jsonify({"message": "Document updated successfully.", "document": doc}), 200

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
