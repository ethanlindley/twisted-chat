import struct


class Packet(object):
    """
        Buffer of data that can be read and written to for communication between sockets across a network
    """

    def __init__(self, buffer=b''):
        self.buffer = buffer

    def retrieve(self):
        return self.buffer

    def read(self, length):
        value = self.buffer[:length]
        self.buffer = self.buffer[length:]
        return value

    def write(self, data):
        self.buffer += data

    # unsigned byte
    def read_byte(self):
        return struct.unpack("<B", self.read(1))[0]

    # unsigned byte
    def write_byte(self, value):
        self.write(struct.pack("<I", value))

    def read_boolean(self):
        return bool(self.read_byte())

    def write_boolean(self, value):
        self.write_byte(int(value))

    # unsigned int
    def read_int(self):
        return struct.unpack("<I", self.read(4))[0]

    # unsigned int
    def write_int(self, value):
        self.write(struct.pack("<I", value))

    # unsigned short
    def read_short(self):
        return struct.unpack("<H", self.read(2))[0]

    # unsigned short
    def write_short(self, value):
        self.write(struct.pack("<H",  value))

    def read_string(self):
        return self.read(length=self.read_short()).decode("utf-8")

    def write_string(self, value):
        self.write_short(len(value))
        self.write(value.encode("utf-8"))


