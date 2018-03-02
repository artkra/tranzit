import re
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
            data = await reader.read(32768)

            type, msg = WebSocketServer.decode_msg(data)

            print(data)
            await asyncio.sleep(0.1)
            print('NEW COROUTINE TO SERVE WEBSOCKET')

    @staticmethod
    def decode_msg(msg):
        byte_data = bytearray(msg)
        b1 = byte_data[0]
        b2 = byte_data[1]
        fin = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN

        masks = byte_data[2:6]

        decoded = ''

        for i in range(payload_length):
            char = byte_data[6 + i]
            char ^= masks[len(decoded) % 4]
            decoded += chr(char)

        return 'text', decoded

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
