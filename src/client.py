from logzero import logger

from twisted.internet import protocol
from twisted.internet.error import ConnectionDone as connectionDone


class Client(protocol.Protocol):
    """
        Client instances are instantiated when the server
        receives an incoming suggestion

        Able to receive and send data across sockets
    """
    def __init__(self):
        self.server = None

    def connectionMade(self):
        self.server = self.factory
        self.server.clients.append(self)
        logger.warning("new client connected")

    def connectionLost(self, reason=connectionDone):
        self.server.clients.remove(self)
        logger.warning("client disconnected, reason: {}".format(reason.getErrorMessage().lower()))

    def dataReceived(self, data):
        logger.debug("data received - {}".format(data))

    def broadcast(self, packet):
        # TODO - route data to all clients connected to our server instance
        pass

    def route(self, packet):
        # TODO - route data to a client
        pass
