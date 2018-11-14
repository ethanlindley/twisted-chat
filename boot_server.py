from twisted.internet import reactor

from network.network_factory import NetworkFactory


if __name__ == "__main__":
    reactor.listenTCP(5001, NetworkFactory())
    reactor.run()
