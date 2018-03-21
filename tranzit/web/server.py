import yaml
from aiohttp import web

from tranzit.web.ws_server import WebSocketServer, TranzitWSHandler


class Server(object):
    def __init__(self, config_file):
        try:
            self.config = yaml.load(open(config_file).read())
            self.http_host = self.config['http_host']
            self.http_port = self.config['http_port']
            self.ws_host = self.config['ws_host']
            self.ws_port = self.config['ws_port']
            self.production = self.config['production']
            self.apps = self.config['apps']

        except Exception:
            print('Error parsing config file.')

    def run(self):
        # collect routes
        # build dictionary of ws rules
        # build injection files
        # set WebSocketServer instance
        # start ws server
        # start http server

        # for app in self.apps:
        #     exec('from .' + app + '.routes import routes')



        app = web.Application()
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
                
        Your app is now running on {}:{}                        
        \033[0m                                     
        """.format(self.http_host, self.http_port))
        web.run_app(app, host=self.http_host, port=self.http_port, print=False)

    def start_ws(self):
        wsserver = WebSocketServer()
        wsserver.run_forever()
