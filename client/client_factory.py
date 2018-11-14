from logzero import logger

from twisted.internet import reactor
from twisted.internet import protocol

from client.client import Client


class ClientFactory(protocol.ClientFactory):
    """
        Responsible for instantiating and keeping track of new clients/connections
        to the network
    """

    protocol = Client

    def startedConnecting(self, connector):
        logger.info("connecting to main network instance...")

    def clientConnectionFailed(self, connector, reason):
        logger.error("unable to establish connection to main network instance, reason: {}".format(
            reason.getErrorMessage().lower()))

    def clientConnectionLost(self, connector, reason):
        logger.warning("connection to main network instance has dropped, reason: {}".format(
            reason.getErrorMessage().lower()))
        # shutdown the main thread
        reactor.stop()
