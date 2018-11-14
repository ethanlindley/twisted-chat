from twisted.internet import reactor

from src.server import ServerFactory


if __name__ == "__main__":
    server = ServerFactory()
    reactor.listenTCP(5001, server)
    reactor.run()
