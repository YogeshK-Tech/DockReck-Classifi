import os
from PyPDF2 import PdfReader
import docx
import zipfile
from PIL import Image
import pytesseract

def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        return text
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return ""

def extract_text_from_docx(filepath):
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
        return ""

def extract_text_from_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT {filepath}: {e}")
        return ""

def extract_text_from_image(filepath):
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading image {filepath}: {e}")
        return ""
    
def extract_text_from_zip(zip_path):
    text = ""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                text += extract_text_from_file(file)
    return text

def extract_text_from_file(file_path):
    file_extension = file_path.rsplit('.', 1)[1].lower()

    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['doc', 'docx']:
        return extract_text_from_docx(file_path)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        return extract_text_from_image(file_path)
    elif file_extension == 'txt':
        return extract_text_from_txt(file_path)
    elif file_extension == 'zip':
        return extract_text_from_zip(file_path)
    else:
        raise ValueError("Unsupported file type.")
