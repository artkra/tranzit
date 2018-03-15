import yaml
from aiohttp import web

from .ws_server import WebSocketServer, WebSocketHandler

class Server():
    def __init__(self, config_file):
        try:
            self.config = yaml.load(open(config_file).read())
            self.http_host = self.config['http_host']
            self.http_port = self.config['http_port']
            self.ws_host = self.config['ws_host']
            self.ws_port = self.config['ws_port']
            self.production = self.config['production']
        except Exception:
            print('Error parsing config file.')

    def run_server(self):
        # collect routes
        # build dictionary of ws rules
        # build injection files
        # set WebSocketServer instance
        # start ws server
        # start http server

        app = web.Application()
        web.run_app(app)
