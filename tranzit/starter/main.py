from tranzit.web import Server


if __name__ == '__main__':
    server = Server('main.yml')
    server.run()
    # server.start_ws()

