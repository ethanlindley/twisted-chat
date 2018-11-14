from logzero import logger

from twisted.internet import protocol

from network.network_client import NetworkClient
from network.database import Database


class NetworkFactory(protocol.ServerFactory):
    """
        Main network instance that all clients connect to

        Create instances of Client objects upon new connections to the socket
    """

    protocol = NetworkClient

    def __init__(self):
        self.clients = list()
        self.db = Database()

        logger.info("starting main network instance...")
