import ast
import base64

from asyncio import Protocol, BaseTransport

from socket import socket
from methods import *

from log import LOGGING_CONFIG
from logging.config import dictConfig
import logging.config

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('server')

class Server(Protocol):
    def __init__(self):
        super().__init__()    
        self.transport = None
    
    def connection_made(self, transport: BaseTransport):
        self.transport = transport

        sock: socket = self.transport.get_extra_info('socket')
        remote_addr = sock.getpeername()

        logger.info(f'new connection made from {remote_addr}')

    def data_received(self, data):
        logger.info('data received')

        data = data.decode('utf-8')

        data = data.split('|')
        method_name = data[0]
        method = METHODS.get(method_name)

        if method:
            try:
                logger.info(f'{method_name} called')
                try:
                    data = data[1].encode()
                    data = base64.b64decode(data).decode('utf-8')
                    data = ast.literal_eval(data)
                except Exception as e:
                    logger.info(str(e))
                    self.write({RESPONSE: 'bad request format'})
                    return
                method(data, self.write, self.transport.close)
                return
            except Exception as e:
                logger.info(str(e))
                self.write({RESPONSE: 'internal server error'})
                return

        response = f'bad request method {method_name} is not known'
        logger.info(response)
        self.write({RESPONSE: response})

    def connection_lost(self, exc: Exception | None):
        self.transport = None

        if exc:
            logger.info(f'an exception occured when closing the connection {exc}')
            return
        
        logger.info('connection closed')

    def eof_received(self):
        logger.info('eof received')
        
        return False
    
    def write(self, data:str):
        data = str(data)
        data = data.encode()
        self.transport.write(data)
