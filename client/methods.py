import os
import tqdm
import ntpath
import base64

from constants import *

def parse_methods(args, send_request):
    if args.signup:
        send_request(
            signup(args.name, args.password)
        )

    elif args.login:
        send_request(
            login(args.name, args.password)
        )

    elif args.logout:
        send_request(
            logout(args.session_id)
        )

    elif args.listing:
        send_request(
            listing(args.session_id)
        )

    elif args.download:
        send_request(
            download(args.session_id, args.file_name)
        )
    
    elif args.upload:
        upload(send_request, args.session_id, args.file_path)

    elif args.history:
        send_request(
            history(args.session_id)
        )

    elif args.search:
        send_request(
            search(args.session_id, args.file_name)
        )

REQUEST = '{method}|{message}'
def genereat_request(method, message):
    message = base64.b64encode(str(message).encode()).decode('utf-8')
    return REQUEST.format(
        method=method, 
        message=message
    )

def signup(name, password):
    return genereat_request(
        SIGNUP,
        {NAME: name, PASSWORD: password}
    )

def login(name, password):
    return genereat_request(
        LOGIN,
        {NAME: name, PASSWORD: password}
    )

def logout(session_id):
    return genereat_request(
        LOGOUT,
        {SESSION_ID: session_id}
    )

def history(session_id):
    return genereat_request(
        HISTORY,
        {SESSION_ID: session_id}
    )

def listing(session_id):
    return genereat_request(
        LISTING,
        {SESSION_ID: session_id}
    )

FILE_CHUNK_SIZE = 10240
def download(session_id, file_name):
    return genereat_request(
        DOWNLOAD,
        {SESSION_ID: session_id, FILE_NAME: file_name}
    )

def upload(send_request, session_id, file_path:str):
    file_name = ntpath.basename(file_path)
    total_size = os.path.getsize(file_path)

    with open(file_path, 'rb') as file:
        with tqdm.tqdm(total=total_size, desc=f"uploading {file_name}", unit='B', unit_scale=True) as pbar:           
            while True:
                file_chunk = file.read(FILE_CHUNK_SIZE)

                if not file_chunk:
                    break

                file_chunk = base64.b64encode(file_chunk).decode('utf-8')

                send_request(
                    genereat_request(
                        UPLOAD,
                        {
                            SESSION_ID: session_id, 
                            FILE_NAME: file_name, 
                            FILE_CHUNK: file_chunk
                        }
                    )
                )
                
                pbar.update(len(file_chunk))

    send_request(
        genereat_request(
            UPLOAD,
            {
                SESSION_ID: session_id, 
                FILE_NAME: file_name, 
                FILE_CHUNK: '0'
            }
        )
    )

def search(session_id, file_name):
    return genereat_request(
        SEARCH,
        {SESSION_ID: session_id, FILE_NAME: file_name}
    )
