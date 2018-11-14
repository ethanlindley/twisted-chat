from logzero import logger

from twisted.internet import protocol

from src.client import Client


class ServerFactory(protocol.ServerFactory):
    """
        Main server instance that all clients connect to

        Create instances of Client objects upon new connections to the socket
    """
    protocol = Client

    def __init__(self):
        self.clients = list()

        logger.info("starting server...")
