import logging
logger = logging.getLogger('server')

from db import *
from constants import *

def signup(data):
    name = data.get(NAME)
    if not name:
        return {RESPONSE:'no name found in request'}
    
    password = data.get(PASSWORD)
    if not password:
        return {RESPONSE:'no password found in request'}

    return signup_user(name, password)

def login(data):
    name = data.get(NAME)
    if not name:
        return {RESPONSE:'no name found in request'}
    
    password = data.get(PASSWORD)
    if not password:
        return {RESPONSE:'no password found in request'}

    return login_user(name, password)
    
def logout(data):
    pass

def history(data):
    pass

def listing(data):
    pass

def download(data):
    pass

def upload(data):
    pass

def search(data):
    pass

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
