import os
from googleapiclient.http import MediaFileUpload
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_or_create_folder(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    response = service.files().list(q=query, fields="files(id, name)").execute()
    files = response.get('files', [])
    
    if files:
        return files[0]['id']
    
    metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        metadata['parents'] = [parent_id]
    
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder['id']

def save_files_to_drive(service, classified_docs):
    """
    Saves files from classified_docs to Google Drive.
    """
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
