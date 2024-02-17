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
            download(args.session_id)
        )
    
    elif args.upload:
        send_request(
            upload(args.session_id)
        )

    elif args.history:
        send_request(
            history(args.session_id)
        )

    elif args.search:
        send_request(
            search(args.session_id)
        )

REQUEST = '{method}|{message}'
def signup(name, password):
    return REQUEST.format(
        method=SIGNUP, 
        message=str({NAME: name, PASSWORD: password})
    )

def login(name, password):
    return REQUEST.format(
        method=LOGIN,
        message=str({NAME: name, PASSWORD: password})
    )

def logout(session_id):
    return REQUEST.format(
        method=LOGOUT,
        message=str({SESSION_ID: session_id})
    )

def history(session_id):
    return REQUEST.format(
        method=HISTORY,
        message=str({SESSION_ID: session_id})
    )

def listing(session_id):
    return REQUEST.format(
        method=LISTING,
        message=str({SESSION_ID: session_id})
    )

def download(session_id, file_name):
    return REQUEST.format(
        method=DOWNLOAD,
        message=str({SESSION_ID: session_id, FILE_NAME: file_name})
    )

def upload(session_id):
    return REQUEST.format(
        method=UPLOAD,
        message=str({SESSION_ID: session_id})
    )

def search(session_id, file_name):
    return REQUEST.format(
        method=DOWNLOAD,
        message=str({SESSION_ID: session_id, FILE_NAME: file_name})
    )
