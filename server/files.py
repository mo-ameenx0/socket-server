import os
from datetime import datetime, timezone, timedelta

USERS_FOLDER = 'users'
DOWNLOAD_HISTORY = 'download_history'

def create_folder(name):
    os.makedirs(os.path.join(USERS_FOLDER, name))
    
    history_file = os.path.join(USERS_FOLDER, name, DOWNLOAD_HISTORY) 
    with open(history_file, 'w') as file:
        file.write('')

def list_user_files(name):
    files = os.listdir(os.path.join(USERS_FOLDER, name))
    if files:
        return files
    else:
        return "no files uploaded yet"

def search_for_file(name, file_name):
    file_path = os.path.join(USERS_FOLDER, name, file_name)

    if os.path.exists(file_path):
        return f"the file {file_name} available for download"
    
    return f'no file with the name {file_name}'

def log_download_history(name, downloaded_file):
    history_file = os.path.join(USERS_FOLDER, name, DOWNLOAD_HISTORY) 

    current_time = datetime.now(timezone(timedelta(hours=3)))

    with open(history_file, 'a') as file:
        file.write(f'{current_time}: {downloaded_file}\n')

def get_file_path(name, file_name):
    return os.path.join(USERS_FOLDER, name, file_name)
