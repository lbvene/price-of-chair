import pymongo

__author__ = 'lbvene'

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    # URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None
    # Don't need init method
    # Self is object's value

    # This method belongs to Database class as whole
    #  and never to instance of Database
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']
        # Database.DATABASE = client.get_default_database

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
