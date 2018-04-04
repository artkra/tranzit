import yaml
from multiprocessing import Process
from importlib.util import spec_from_file_location, module_from_spec
from aiohttp import web

from tranzit.web.ws_server import WebSocketServer, TranzitWSHandler


class MainServer(object):
    def __init__(self, config_file, PROJECT_DIR):
        try:
            self.config = yaml.load(open(config_file).read())
            self.http_host = self.config.get('http_host', '0.0.0.0')
            self.http_port = self.config.get('http_port', 3000)
            self.ws_server_on = self.config.get('ws_server_on', True)
            self.ws_host = self.config.get('ws_host', '0.0.0.0')
            self.ws_port = self.config.get('ws_port', 19719)
            self.ws_rules = {}
            self.production = self.config.get('production', False)
            self.apps = self.config.get('apps', [])
            self.PROJECT_DIR = PROJECT_DIR
            self.main_server = web.Application()
            self.ws_server = None
            self.camel = self.config.get('camel', True)

        except Exception:
            print('Error parsing config file.')

    def run(self):
        # build dictionary of ws rules
        # build injection files

        main_t = Process(target=self.start_main_server)
        main_t.start()

        if self.ws_server_on:
            ws_t = Process(target=self.start_ws_server)
            ws_t.start()

    def start_main_server(self):

        for app in self.apps:
            try:
                spec = spec_from_file_location(app, self.PROJECT_DIR + '/apps/' + app + '/routes.py')
                module = module_from_spec(spec)
                spec.loader.exec_module(module)

                prefix = module.PATH_PREFIX
                routes = module.routes

                for route in routes:
                    self.main_server.router.add_route('GET', prefix + route, routes[route]().get)
                    self.main_server.router.add_route('POST', prefix + route, routes[route]().post)
                    self.main_server.router.add_route('PUT', prefix + route, routes[route]().put)
                    self.main_server.router.add_route('DELETE', prefix + route, routes[route]().delete)

            except Exception as e:
                print(str(e))
                print('Couldn\'t load app: {}'.format(app))

        if self.camel:
                print("""
        \033[95m         
        TRANZIT STARTING ....


                           shsos/-                                    
                         .os+/++oy/`                                  
                     `-+so++o+o+++o+///-.            `+o-...`         
                   :+sys:::+ooosoo++++yddy-         :dydohs/yy`       
                 `:/:/+syo/://+++oo+///hddd+`     `+yhymho:-`.        
                 sys++osdNdhyysso+oo++/+hyo+:....-::ohy-              
                `NNmNdhy+mNNNmddhhhyyhsooso/os/::/+sy/`               
                -NMNmmmdhoNNmmmmmmddmmhssyhhddhssy+:                  
                /NMMmdmdddsymmmmmddmdhyohy/-://:.              Arabskaja nooooooch....       
                +NMN/+mdhh.  .://osyydho-                             
                hNh- +dh+            yy+                              
               +md`  hdy`            oy/                              
              :md-  /do.             /++                              
               dh    +d:            `oos                              
               /y     -s`         `-:-:s                              
               `d      -s`    `///.    y`                             
                hs`     /s.   :/`      so`                            
                .-:.     .-`           --..   

        \033[0m                                     
            """)

        print('\033[95mYour app is now running at {}:{}\n\n\033[0m'.format(
            self.http_host, self.http_port
        ))

        print('\033[95mWebsocket server ON: {}\n'
              'Websocket server HOST: {}\n'
              'Websocket server PORT: {}\n'
              'Production: {}\n'
              'Working apps: {}\n\033[0m'.format(
                    self.ws_server_on, self.ws_host, self.ws_port,
                    self.production, self.apps
              ))

        web.run_app(self.main_server, host=self.http_host, port=self.http_port, print=False)

    def start_ws_server(self):
        for app in self.apps:
            try:
                spec = spec_from_file_location(app, self.PROJECT_DIR + '/apps/' + app + '/routes.py')
                module = module_from_spec(spec)
                spec.loader.exec_module(module)

                prefix = module.PATH_PREFIX
                ws_rules = module.ws_rules

                self.ws_rules = {**self.ws_rules, **ws_rules}

            except Exception as e:
                print(str(e))
                print('Couldn\'t load app: {}'.format(app))

        self.ws_server = WebSocketServer(
            host=self.ws_host,
            port=self.ws_port,
            api=TranzitWSHandler(rules=self.ws_rules)
        )

        self.ws_server.run_forever()


class TZView(object):

    async def get(self, request):
        return web.Response(text='')

    async def post(self, request):
        return web.Response(text='')

    async def put(self, request):
        return web.Response(text='')

    async def delete(self, request):
        return web.Response(text='')
