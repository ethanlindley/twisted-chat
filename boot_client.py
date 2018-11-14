from twisted.internet import reactor

from client.client_factory import ClientFactory


if __name__ == "__main__":
    reactor.connectTCP('127.0.0.1', 5001, ClientFactory())
    reactor.run()
