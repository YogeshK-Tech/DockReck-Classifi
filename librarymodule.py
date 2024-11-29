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

def upload_file_to_drive(service, file_path, category, subcategory):
    root_folder = get_or_create_folder(service, 'AppName Library')
    category_folder = get_or_create_folder(service, category, root_folder)
    subcategory_folder = get_or_create_folder(service, subcategory, category_folder)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [subcategory_folder]
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
