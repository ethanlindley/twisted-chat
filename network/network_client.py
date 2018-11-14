from logzero import logger

from passlib.hash import pbkdf2_sha256

from twisted.internet import protocol
from twisted.internet.error import ConnectionDone as connectionDone

from libs.packet import Packet
from libs.packet_types import PacketTypes


class NetworkClient(protocol.Protocol):
    """
        Client instances are instantiated when the network
        receives an incoming suggestion

        Able to receive and send data across sockets
    """

    def __init__(self):
        self.server = None

    def connectionMade(self):
        self.server = self.factory
        self.server.clients.append(self)
        logger.warning("new client connected to main network instance")

    def connectionLost(self, reason=connectionDone):
        self.server.clients.remove(self)
        logger.warning("connection to main network instance lost, reason: {}".format(reason.getErrorMessage().lower()))

    def dataReceived(self, data):
        logger.debug("data received - {}".format(data))

        # instantiate a packet object using the data we just received
        data = Packet(data)
        # retrieve the message header
        msg = data.read_int()

        if msg == PacketTypes.CLIENT_HANDSHAKE_REQ.value:
            self.handle_handshake_req()
        elif msg == PacketTypes.CLIENT_LOGIN_REQ.value:
            self.handle_login_req(data)
        elif msg == PacketTypes.CLIENT_REGISTER_REQ.value:
            self.handle_register_req(data)
        else:
            logger.warning("rogue message type received - {}".format(msg))

    def route(self, data):
        # in case we are trying to send a Packet object
        if hasattr(data, "retrieve"):
            # return the buffer
            data = data.retrieve()

        if not type(data) == bytes:
            raise Exception("can't route data - make sure data is a bytes or Packet object")

        logger.debug("sending data - {}".format(data))
        self.transport.write(data)

    def handle_handshake_req(self):
        logger.debug("got handshake request")

        data = Packet()
        data.write_int(PacketTypes.SERVER_HANDSHAKE_RESP.value)
        # successful handshake
        data.write_boolean(1)

        logger.debug("sending handshake response")
        return self.route(data)

    def handle_login_req(self, data):
        logger.debug("got login request")

        username = data.read_string()
        password = data.read_string()

        for user in self.server.db.collection.find():
            _username = user['username']
            _password = user['password']
            if _username == username and pbkdf2_sha256.verify(password, _password):
                # yay! we've found the user's account in the database - let's go ahead and let them through
                _data = Packet()
                _data.write_int(PacketTypes.SERVER_LOGIN_RESP.value)
                _data.write_boolean(1)

                logger.debug("sending login response")
                return self.route(_data)
        _data = Packet()
        _data.write_int(PacketTypes.SERVER_LOGIN_RESP.value)
        # we were unable to find the user's account in the database
        _data.write_boolean(0)

        logger.debug("sending login response")
        return self.route(_data)

    def handle_register_req(self, data):
        logger.debug("got register request")

        username = data.read_string()
        password = data.read_string()

        for user in self.server.db.collection.find():
            _username = user['username']
            if _username == username:
                # oh. they're trying to register but already exist in the database?
                # let's log them in instead
                self.handle_login_req(data)
        self.server.db.add_user(username, password)

        _data = Packet()
        _data.write_int(PacketTypes.SERVER_REGISTER_RESP.value)
        _data.write_boolean(1)

        self.route(_data)
