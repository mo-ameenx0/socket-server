import argparse
import socket
import sys
import os

from dotenv import load_dotenv
load_dotenv()

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

from constants import *
from methods import *

def get_args(args=None):
    parser = argparse.ArgumentParser(description='Client side for socket server.')

    # Group for authentication actions
    auth_group = parser.add_argument_group('Authentication')
    auth_group.add_argument('--signup', action='store_true', help='Sign up for a new account.')
    auth_group.add_argument('--login', action='store_true', help='Log in to an existing account.')
    auth_group.add_argument('--logout', action='store_true', help='Log out of the current session.')
    auth_group.add_argument('--name', type=str, help='Specify the user name. Used for signup and login.')
    auth_group.add_argument('--password', type=str, help='Specify the user password. Required for signup and login.')
    auth_group.add_argument('--session_id', type=str, help='Provide the session ID for authenticated actions.')

    # Group for file operations
    file_group = parser.add_argument_group('File Operations')
    file_group.add_argument('--listing', action='store_true', help='List all available files.')
    file_group.add_argument('--download', action='store_true', help='Download a specified file. Requires --file_name.')
    file_group.add_argument('--upload', action='store_true', help='Upload a new file. Requires --file_path.')
    file_group.add_argument('--file_path', type=str, help='Specify the path of the file for uploading.')
    file_group.add_argument('--file_name', type=str, help='Specify the name of the file for downloading.')

    # Miscellaneous actions
    parser.add_argument('--history', action='store_true', help='View the user\'s action history.')
    parser.add_argument('--search', action='store_true', help='Search for files using the specified query string.')
    parser.add_argument('--persistent', action='store_true', help='Enable a persistent connection for the session.')
    parser.add_argument('--useargs', action='store_true', help='Use the arguments with persistent connections. Requires --persistent.')


    args = parser.parse_args(args)

    # Check for arguments' dependencies
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.useargs and not args.persistent:
        parser.error('--useargs requires --persistent to be set.')

    if args.useargs:
        return args

    if args.signup or args.login:
        if not args.name or not args.password:
            parser.error('--signup and --login require --name and --password.')
    
    if args.logout or args.listing or args.download or args.upload or args.history or args.search:
        if not args.session_id:
            parser.error('--logout, --listing, --download, --upload, --history, and --search require --session_id.')
    
    if args.upload and not args.file_path:
        parser.error('--upload requires --file_path.')
    
    if args.download and not args.file_name:
        parser.error('--download requires --file_name.')

    if args.search and not args.file_name:
        parser.error('--search requires --file_name.')

    return args

def send_request(request:str):
    from time import sleep
    sleep(0.01)
    client.sendall(request.encode('utf-8'))


RECEIVE_BUFFER_SIZE = 1024
def main():
    global client
    args = get_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, int(PORT)))
        
        if not args.persistent:
            parse_methods(args, send_request, client.recv)
            response = client.recv(RECEIVE_BUFFER_SIZE)
            print(response)
            return

        while True:
            if args.useargs:
                user_args = input('enter your args:\n')
                user_args = user_args+" --persistent --useargs"
                args = get_args(user_args.split())
                parse_methods(args, send_request, client.recv)
                response = client.recv(RECEIVE_BUFFER_SIZE)
                print(response, end='\n\n')
            else:
                raw_request = input('enter your request:\n')
                send_request(raw_request)
                response = client.recv(RECEIVE_BUFFER_SIZE)
                print(response, end='\n\n')

if __name__ == '__main__':
    sys.exit(main())
