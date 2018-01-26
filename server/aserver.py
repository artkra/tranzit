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
        self.host = str(host)
        self.port = int(port)
        self.clients = dict()

    async def handle(self, reader, writer):
        res_message = None
        addr = writer.get_extra_info('peername')
        client_id = sha1((addr[0] +
                                  str(addr[1])).encode()).hexdigest()

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
        print('got msg from  {}:\n{}'.format(addr, message))
            
        # if not self.clients[client_id]['handshaken']:
            # res_message = self.handshake(message)
        res_message = '123'
        # if not self.clients[client_id]['alive']:
            # self.close(client_id)

        if res_message:
            print('message!')
            self.clients[client_id]['writer'].write(res_message.encode())
            await writer.drain()
            # writer.close()
                 
    def handshake(self, message):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        key = WebSocketServer.parse_key(message)
        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip().decode('ASCII')

        response_msg = \
           'HTTP/1.1 101 Switching Protocols\r\n' \
           'Upgrade: websocket\r\n'               \
           'Connection: Upgrade\r\n'              \
           'Sec-WebSocket-Accept: {}\r\n'         \
           '\r\n'.format(response_key) 

        return response_msg

    @staticmethod
    def parse_key(message):
        return '123'
    
    def close(self, writer):
        pass

    def handle_request(self, client_id):
        pass

    def run_forever(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle,
                                    self.host,
                                    self.port,
                                    loop=loop)
        server = loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == '__main__':
    wsserver = WebSocketServer('127.0.0.1', 3000)
    wsserver.run_forever()
