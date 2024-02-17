import os
import jwt
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

SECRET = os.environ.get('SECRET')

import logging
logger = logging.getLogger('server')

from db import *
from constants import *

def required_keys(keys=[NAME, PASSWORD]):
    def decorator(func):
        @wraps(func)
        def wrapped_function(request):            
            for key in keys:
                if not key in request.keys():
                    return {RESPONSE: f'the request is missing {key}'}

                value = request.get(key)
                if value is None or value == '':
                    return {RESPONSE: f'the value for {key} is not valid'}

            return func(request)
        return wrapped_function
    return decorator

def verify_session_id(func):
    def wrapper(request):
        session_id = request.get(SESSION_ID)

        try:
            if is_user_loged_out(session_id):
                return {RESPONSE: 'user already loged out'}
            
            decoded_session_id = jwt.decode(session_id, SECRET, algorithms=['HS256'])
        except Exception as e:
            delete_user_session(session_id)
            if isinstance(e, jwt.ExpiredSignatureError):
                return {RESPONSE: 'login again the session id has expired'}
            return {RESPONSE: 'the session id is not valid'}

        request[SESSION_ID] = decoded_session_id

        return func(request)
    
    return wrapper


@required_keys([NAME, PASSWORD])
def signup(request):
    name = request.get(NAME)
    password = request.get(PASSWORD)

    return signup_user(name, password)



@required_keys([NAME, PASSWORD])
def login(request):
    name = request.get(NAME)
    password = request.get(PASSWORD)

    return login_user(name, password)



@required_keys([SESSION_ID])
@verify_session_id
def logout(request):
    session_id = request.get(SESSION_ID)

    user_id = session_id.get(USER_ID)
    name = session_id.get(NAME)

    return logout_user(name, user_id)


@required_keys([SESSION_ID])
@verify_session_id
def history(request):
    session_id = request.get(SESSION_ID)



@required_keys([SESSION_ID])
@verify_session_id
def listing(request):
    session_id = request.get(SESSION_ID)



@required_keys([SESSION_ID, FILE_NAME])
@verify_session_id
def download(request):
    session_id = request.get(SESSION_ID)



@required_keys([SESSION_ID])
@verify_session_id
def upload(request):
    session_id = request.get(SESSION_ID)



@required_keys([SESSION_ID])
@verify_session_id
def search(request):
    session_id = request.get(SESSION_ID)



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
