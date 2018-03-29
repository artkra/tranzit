import os
from tranzit.web import MainServer

PROJECT_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    server = MainServer('main.yml', PROJECT_DIR)
    server.run()


