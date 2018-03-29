import yaml
from multiprocessing import Process
from importlib.util import spec_from_file_location, module_from_spec
from aiohttp import web

from tranzit.web.ws_server import WebSocketServer, TranzitWSHandler


class MainServer(object):
    def __init__(self, config_file, PROJECT_DIR):
        try:
            self.config = yaml.load(open(config_file).read())
            self.http_host = self.config['http_host']
            self.http_port = self.config['http_port']
            self.ws_server_on = self.config['ws_server_on']
            self.ws_host = self.config['ws_host']
            self.ws_port = self.config['ws_port']
            self.production = self.config['production']
            self.apps = self.config['apps']
            self.PROJECT_DIR = PROJECT_DIR

        except Exception:
            print('Error parsing config file.')

    def run(self):
        # collect routes
        # build dictionary of ws rules
        # build injection files

        main_t = Process(target=self.start_main_server)
        main_t.start()

        if self.ws_server_on:
            ws_t = Process(target=self.start_ws_server)
            ws_t.start()

    def start_main_server(self):
        server = web.Application()

        for app in self.apps:
            try:
                spec = spec_from_file_location(app, self.PROJECT_DIR + '/apps/' + app + '/routes.py')
                module = module_from_spec(spec)
                spec.loader.exec_module(module)

                prefix = module.PATH_PREFIX
                routes = module.routes

                for route in routes:
                    server.router.add_route('GET', prefix + route, routes[route]().get)
                    server.router.add_route('POST', prefix + route, routes[route]().post)
                    server.router.add_route('PUT', prefix + route, routes[route]().put)
                    server.router.add_route('DELETE', prefix + route, routes[route]().delete)

            except Exception as e:
                raise(e)
                print('Couldn\'t load app: {}'.format(app))

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

        web.run_app(server, host=self.http_host, port=self.http_port, print=False)

    def start_ws_server(self):
        wsserver = WebSocketServer(
            host=self.ws_host,
            port=self.ws_port,
            api=TranzitWSHandler(rules={})
        )
        wsserver.run_forever()


class TZView(object):

    async def get(self, request):
        return web.Response(text='')

    async def post(self, request):
        return web.Response(text='')

    async def put(self, request):
        return web.Response(text='')

    async def delete(self, request):
        return web.Response(text='')
