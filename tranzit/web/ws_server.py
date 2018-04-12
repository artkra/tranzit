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


class TranzitWSHandler(object):
    def __init__(self, rules={}):
        self.rules = rules

    async def handle_text(self, loop, writer, msg):
        try:
            body = msg.split('|')
            func = body[0]
            params = body[1].split(',')
        except IndexError as e:
            # wrong message format
            print('wrong message format: {}'.format(msg))
        except Exception as e:
            print('Error in WS message: {} - {}'.format(msg, str(e)))

        if func in self.rules:
            try:
                asyncio.ensure_future(
                    self.rules[func](*params, send_func=WebSocketServer.send_text, writer=writer),
                    loop=loop
                )

            except Exception as e:
                print('Error in WS rule \'{}\': {}'.format(func, str(e)))

        else:
            await WebSocketServer.send_text(writer, msg)

    async def handle_binary(self, loop, writer, msg):
        pass

    async def handle_buffered(self, loop, reader, writer, first_msg):
        pass


class WebSocketServer(object):
    def __init__(self, host='0.0.0.0', port=19719, api=TranzitWSHandler()):
        self.loop = asyncio.get_event_loop()
        self.host = host
        self.port = int(port)
        self.clients = dict()
        self.API = api

    async def handle(self, reader, writer):
        addr = writer.get_extra_info('peername')
        client_id = sha1((addr[0] + str(addr[1])).encode()).hexdigest()

        if client_id not in self.clients.keys():
            self.clients[client_id] = {
                'handshaken': False,
                'addr': addr,
                'writer': writer,
                'reader': reader
            }

        data = await reader.read(2048)
        message = data.decode()
            
        handshake_msg = WebSocketServer.handshake(message)

        if handshake_msg:
            self.clients[client_id]['handshaken'] = True
            writer.write(handshake_msg.encode())
            await writer.drain()

            fut = asyncio.Future()

            asyncio.ensure_future(self.serve_wsocket(fut, client_id), loop=self.loop)

            try:
                res = await asyncio.wait_for(fut, timeout=3600)
            except asyncio.TimeoutError as e:
                writer.close()
                self.clients.pop(client_id)

    async def serve_wsocket(self, fut, client_id):
        reader = self.clients[client_id]['reader']
        writer = self.clients[client_id]['writer']

        try:
            while True:
                b1, b2 = await reader.read(2)
                fin = b1 & FIN
                opcode = b1 & OPCODE
                masked = b2 & MASKED
                payload_length = b2 & PAYLOAD_LEN

                buffered_msg = ''

                if payload_length == 126:
                    b3 = await reader.read(2)
                    payload_length = struct.unpack('>H', b3)[0]
                if payload_length == 127:
                    b3 = await reader.read(8)
                    payload_length = struct.unpack('>Q', b3)[0]

                masks = await reader.read(4)

                decoded = ''

                msg = await reader.read(payload_length)

                for char in msg:
                    char ^= masks[len(decoded) % 4]
                    decoded += chr(char)

                if opcode == OPCODE_CLOSE_CONN:
                    # client asked to close connection, close this
                    writer.close()
                    fut.set_result(0)
                if not masked:
                    # not allowed, close this
                    writer.close()
                    fut.set_result(0)
                if opcode == OPCODE_CONTINUATION:
                    # handle buffering
                    await self.API.handle_buffered(self.loop, reader, writer, decoded)

                elif opcode == OPCODE_BINARY:
                    # handle binary data
                    await self.API.handle_binary(self.loop, writer, decoded)

                elif opcode == OPCODE_TEXT:
                    # handle text
                    await self.API.handle_text(self.loop, writer, decoded)

                elif opcode == OPCODE_PONG:
                    pass
        except Exception as e:
            print(str(e))
            writer.close()
            self.clients.pop(client_id)

    @staticmethod
    async def send_text(writer, msg):
        header = bytearray()
        payload = msg.encode('utf-8')
        payload_length = len(payload)

        if payload_length <= 125:
            header.append(FIN | OPCODE_TEXT)
            header.append(payload_length)

        elif payload_length >= 126 and payload_length <= 65535:
            header.append(FIN | OPCODE_TEXT)
            header.append(PAYLOAD_LEN_EXT16)
            header.extend(struct.pack(">H", payload_length))

        elif payload_length < 18446744073709551616:
            header.append(FIN | OPCODE_TEXT)
            header.append(PAYLOAD_LEN_EXT64)
            header.extend(struct.pack(">Q", payload_length))

        else:
            print('Too big message')
            return

        writer.write(header + payload)

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
    ws_server = WebSocketServer('0.0.0.0', 3333)
    ws_server.run_forever()
