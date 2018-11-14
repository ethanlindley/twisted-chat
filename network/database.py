from logzero import logger

from passlib.hash import pbkdf2_sha256

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Database(object):
    """
        Responsible for retrieving and manipulating data from the network's database
    """

    def __init__(self):
        # TODO - parse config values from JSON config file (or similar structure)
        self.connection = MongoClient('localhost', 27017)
        try:
            # ismaster command is cheap and does not require auth
            self.connection.admin.command('ismaster')
        except ConnectionFailure:
            raise ConnectionFailure("unable to establish a connection to the MongoDB server")
        self.database = self.connection['twisted-chat']
        self.collection = self.database['twisted-chat']

    def add_user(self, username, password):
        # TODO - beef encryption, add uid system
        user = {
            "username": username,
            "password": pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        }
        logger.debug("adding user - {}".format(user))
        return self.collection.insert_one(user)

    def find_by_uid(self, uid):
        return self.collection.find_one({"_id": uid})
