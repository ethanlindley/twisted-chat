from logzero import logger

from twisted.internet import reactor
from twisted.internet import protocol

from libs.packet import Packet
from libs.packet_types import PacketTypes


class Client(protocol.Protocol):
    """
        Backend client protocol
    """

    def connectionMade(self):
        logger.info("successfully connected to main network instance")
        self.init_handshake_req()

    def dataReceived(self, data):
        logger.debug("data received - {}".format(data))

        # instantiate a packet object using the data we just received
        data = Packet(data)
        # retrieve the message header
        msg = data.read_int()

        if msg == PacketTypes.SERVER_HANDSHAKE_RESP.value:
            self.handle_handshake_resp(data)
        elif msg == PacketTypes.SERVER_LOGIN_RESP.value:
            self.handle_login_resp(data)
        elif msg == PacketTypes.SERVER_REGISTER_RESP.value:
            self.handle_register_resp(data)
        elif msg == PacketTypes.CLIENT_GO_GET_LOST.value:
            self.handle_client_eject()
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

    def init_handshake_req(self):
        data = Packet()
        data.write_int(PacketTypes.CLIENT_HANDSHAKE_REQ.value)

        logger.debug("sending handshake request...")
        return self.route(data)

    def handle_handshake_resp(self, data):
        resp_code = data.read_boolean()

        if resp_code is True:
            choice = input("Please enter 1 for login, 2 for registration: ")
            if int(choice) == 1:
                self.init_login_req()
            else:
                self.init_register_req()
        else:
            raise Exception("unsuccessful handshake")

    def init_login_req(self):
        username = input("username: ")
        password = input("password: ")

        data = Packet()
        data.write_int(PacketTypes.CLIENT_LOGIN_REQ.value)
        data.write_string(username)
        data.write_string(password)

        logger.debug("sending login request...")
        self.route(data)

    def handle_login_resp(self, data):
        resp_code = data.read_boolean()

        if resp_code is True:
            logger.info("successfully logged in")
        else:
            logger.error("unable to login - double check your login details and try again")
            self.init_login_req()

    def init_register_req(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        data = Packet()
        data.write_int(PacketTypes.CLIENT_REGISTER_REQ.value)
        data.write_string(username)
        data.write_string(password)

        logger.debug("sending register request")
        self.route(data)

    def handle_register_resp(self, data):
        resp_code = data.read_boolean()

        if resp_code is True:
            logger.info("user successfully registered, now logging in")
            self.init_login_req()
        else:
            logger.error("unable to register user in database")

    def handle_client_eject(self):
        reactor.callFromThread(reactor.stop)
