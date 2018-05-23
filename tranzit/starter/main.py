import os
from tranzit.web import MainServer

PROJECT_DIR = os.getcwd()

if __name__ == '__main__':
    server = MainServer('server.yml', PROJECT_DIR)
    server.run()


