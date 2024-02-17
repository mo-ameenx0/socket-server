import os
import base64
import jwt
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

SECRET = os.environ.get('SECRET')

import logging
logger = logging.getLogger('server')

from files import *
from db import *
from constants import *

def required_keys(keys=[NAME, PASSWORD]):
    def decorator(func):
        @wraps(func)
        def wrapped_function(request, write, close):      
            for key in keys:
                if not key in request.keys():
                    write({RESPONSE: f'the request is missing {key}'})
                    close()
                    return

                value = request.get(key)
                if value is None or value == '':
                    write({RESPONSE: f'the value for {key} is not valid'})
                    close()
                    return

            return func(request, write, close)
        return wrapped_function
    return decorator

def verify_session_id(func):
    def wrapper(request, write, close):
        session_id = request.get(SESSION_ID)

        try:            
            decoded_session_id = jwt.decode(session_id, SECRET, algorithms=['HS256'])
        except Exception as e:
            delete_user_session(session_id)
            if isinstance(e, jwt.ExpiredSignatureError):
                write({RESPONSE: 'login again the session id has expired'})
                close()
                return
            write({RESPONSE: 'the session id is not valid'})
            close()
            return
        
        request[SESSION_ID] = decoded_session_id

        return func(request, write, close)
    
    return wrapper


@required_keys([NAME, PASSWORD])
def signup(request, write, close):
    name = request.get(NAME)
    password = request.get(PASSWORD)

    write(
        signup_user(name, password)
    )



@required_keys([NAME, PASSWORD])
def login(request, write, close):
    name = request.get(NAME)
    password = request.get(PASSWORD)

    write(login_user(name, password))



@required_keys([SESSION_ID])
@verify_session_id
def logout(request, write, close):
    session_id = request.get(SESSION_ID)

    user_id = session_id.get(USER_ID)
    name = session_id.get(NAME)

    write(logout_user(name, user_id))


@required_keys([SESSION_ID])
@verify_session_id
def history(request, write, close):
    session_id = request.get(SESSION_ID)



@required_keys([SESSION_ID])
@verify_session_id
def listing(request, write, close):
    session_id = request.get(SESSION_ID)

    name = session_id.get(NAME)

    write(list_user_files(name))



@required_keys([SESSION_ID, FILE_NAME])
@verify_session_id
def download(request, write, close):
    session_id = request.get(SESSION_ID)

    name = session_id.get(NAME)
    file_name = request.get(FILE_NAME)

    log_download_history(name, file_name)

    file_path = get_file_path(name, file_name)

    if not os.path.exists(file_path):
        write({RESPONSE: 'closing download'})
        write({RESPONSE: f'no file with the name {file_name}'})
        close()
        return
    
    with open(get_file_path(name, file_name), 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            write(data)

        close()

@required_keys([SESSION_ID, FILE_NAME, FILE_CHUNK])
@verify_session_id
def upload(request, write, close):
    session_id = request.get(SESSION_ID)

    name = session_id.get(NAME)
    file_name = request.get(FILE_NAME)
    file_chunk = request.get(FILE_CHUNK)


    if file_chunk == '0':
        write('file upload completed')
        return

    file_chunk = base64.b64decode(file_chunk.encode())

    file_path = get_file_path(name, file_name)

    with open(file_path, 'ab+') as file:
        file.write(file_chunk)

@required_keys([SESSION_ID, FILE_NAME])
@verify_session_id
def search(request, write, close):
    session_id = request.get(SESSION_ID)

    name = session_id.get(NAME)
    file_name = request.get(FILE_NAME)

    write({RESPONSE: search_for_file(name, file_name)})


METHODS = {
    SIGNUP:signup,
    LOGIN:login,
    LOGOUT:logout,
    HISTORY:history,
    LISTING:listing,
    DOWNLOAD:download,
    UPLOAD:upload,
    SEARCH:search
}
