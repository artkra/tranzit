import re
import struct
import asyncio
from hashlib import sha1
from base64 import b64encode


FIN                 = 0x80
OPCODE              = 0x0f
MASKED              = 0x80
PAYLOAD_LEN         = 0x7f
PAYLOAD_LEN_EXT16   = 0x7e
PAYLOAD_LEN_EXT64   = 0x7f

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT         = 0x1
OPCODE_BINARY       = 0x2
OPCODE_CLOSE_CONN   = 0x8
OPCODE_PING         = 0x9
OPCODE_PONG         = 0xA


class WebSocketServer():
    def __init__(self, host, port):
        self.loop = asyncio.get_event_loop()
        self.host = str(host)
        self.port = int(port)
        self.clients = dict()

    async def handle(self, reader, writer):
        addr = writer.get_extra_info('peername')
        client_id = sha1((addr[0] + str(addr[1])).encode()).hexdigest()

        if client_id not in self.clients.keys():
            self.clients[client_id] = {
                'alive': True,
                'handshaken': False,
                'addr': addr,
                'writer': writer,
                'reader': reader
            }

        data = await reader.read(32768)
        message = data.decode()
            
        handshake_msg = WebSocketServer.handshake(message)

        if handshake_msg:
            self.clients[client_id]['handshaken'] = True
            writer.write(handshake_msg.encode())
            await writer.drain()

            self.loop.create_task(self.serve_wsocket(client_id))

    async def serve_wsocket(self, client_id):
        reader = self.clients[client_id]['reader']
        writer = self.clients[client_id]['writer']
#todo: decode/encode messages, create API class for handling messages
        while True:
            b1, b2 = await reader.read(2)
            fin = b1 & FIN
            opcode = b1 & FIN
            masked = b2 & MASKED
            payload_length = b2 & PAYLOAD_LEN

            buffered_msg = ''

            if payload_length == 126:
                b3 = await reader.read(2)
                payload_length = struct.unpack('>H', b3)[0]
            if payload_length == 127:
                b3 = await reader.read(8)
                payload_length = struct.unpack('>Q', b3)[0]

            if not b1:
                # connection closed, close this
                writer.close()
                return
            if opcode == OPCODE_CLOSE_CONN:
                # client asked to close connection, close this
                writer.close()
                return
            if not masked:
                # not allowed, close this
                writer.close()
                return
            if opcode == OPCODE_CONTINUATION:
                # handle buffering
                pass
            elif opcode == OPCODE_BINARY:
                # handle binary data
                pass
            elif opcode == OPCODE_TEXT:
                # handle text
                pass
            elif opcode == OPCODE_PING:
                # handle ping
                pass
            elif opcode == OPCODE_PONG:
                # handle pong
                pass
            else:
                # unknown, close this
                return

            masks = await reader.read(4)

            decoded = ''

            msg = await reader.read(payload_length)

            for char in msg:
                char ^= masks[len(decoded) % 4]
                decoded += chr(char)

    @staticmethod
    def handshake(message):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        key = re.search('\n[sS]ec-[wW]eb[sS]ocket-[kK]ey[\s]*:[\s]*(.*)\r\n', message)

        if key:
            key = key.group(1)

        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip().decode('ASCII')

        response_msg = \
           'HTTP/1.1 101 Switching Protocols\r\n' \
           'Upgrade: websocket\r\n'               \
           'Connection: Upgrade\r\n'              \
           'Sec-WebSocket-Accept: {}\r\n'         \
           '\r\n'.format(response_key) 

        return response_msg

    def close(self, writer):
        pass

    def run_forever(self):
        coro = asyncio.start_server(self.handle, self.host, self.port, loop=self.loop)
        server = self.loop.run_until_complete(coro)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        self.loop.run_until_complete(server.wait_closed())
        self.loop.close()


if __name__ == '__main__':
    wsserver = WebSocketServer('127.0.0.1', 3000)
    wsserver.run_forever()
