import os
from tranzit.web import Server

PROJECT_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    server = Server('main.yml', PROJECT_DIR)
    server.run()
    # server.start_ws()

