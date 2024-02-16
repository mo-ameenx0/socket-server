import argparse
import socket
import sys
import os

from dotenv import load_dotenv
load_dotenv()

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

SIGNUP = 'signup'
LOGIN = 'login'
LOGOUT = 'logout'
HISTORY = 'history'
LISTING = 'listing'
DOWNLOAD = 'download'
UPLOAD = 'upload'
SEARCH = 'search'

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, int(PORT)))
        s.sendall(b'login|{"name":"tesdfdfting", "password":"sadfa2rf3"}')
        test = s.recv(1024)
        print(test)
        

if __name__ == '__main__':
    sys.exit(main())
