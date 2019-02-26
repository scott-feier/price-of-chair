import pymongo


class Database(object):
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):  # returns cursor
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_all(collection):  # returns cursor
        return Database.DATABASE[collection].find()

    @staticmethod
    def find_one(collection, query):  # returns JSON object
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, obj_id, data):  # updates JSON object
        return Database.DATABASE[collection].update({"_id": obj_id}, data)

    @staticmethod
    def update1(collection, query, data):  # updates JSON object
        return Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def delete(collection, query):  # updates JSON object
        return Database.DATABASE[collection].delete_one(query)
