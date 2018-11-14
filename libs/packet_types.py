from enum import Enum


class PacketTypes(Enum):
    CLIENT_GO_GET_LOST = 0

    CLIENT_HANDSHAKE_REQ = 1
    SERVER_HANDSHAKE_RESP = 2

    CLIENT_LOGIN_REQ = 3
    SERVER_LOGIN_RESP = 4