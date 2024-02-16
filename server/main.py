
import asyncio
import socket
import os
import sys

from server import Server

from dotenv import load_dotenv
load_dotenv()

async def main():   
    loop = asyncio.get_event_loop()
    server = await loop.create_server(
        protocol_factory=Server,
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
        family=socket.AF_INET,
    )
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
    