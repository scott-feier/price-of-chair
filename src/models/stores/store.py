import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.stores.errors as store_errors
import src.models.stores.constants as store_constants
from urllib.parse import urlsplit, urlunsplit


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.query = query
        self.tag_name = tag_name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Store {} at website {}>'.format(self.name, self.url_prefix)

        #  Amazon <span id="priceblock_ourprice" class="a-size-medium a-color-price">$629.00</span>
    def jsonU(self):
        return {
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    def json(self):
        x = self.jsonU()
        x.update({
            "_id": self._id
        })
        return x

    def save_to_db(self):
        Database.insert(store_constants.COLLECTION, self.json())

    def update_to_db(self):
        Database.update(store_constants.COLLECTION, self._id, self.jsonU())

    @staticmethod
    def get_from_db_by_name(name):
        store_data = Database.find_one(store_constants.COLLECTION, {'name': name})
        return store_data  # returns database record, fine if checking for presence / absence

    @staticmethod
    def get_from_db_by_id(_id):
        store_data = Database.find_one(store_constants.COLLECTION, {'_id': _id})
        return store_data  # returns database record, fine if checking for presence / absence

    @classmethod
    def get_obj_from_db_by_id(cls, _id):
        store_data = Database.find_one(store_constants.COLLECTION, {'_id': _id})

        if store_data:
            store_data = cls(**store_data)
        return store_data  # returns store object or None

    @classmethod
    def get_all_store_obj_from_db(cls):
        store_data = Database.find_all(store_constants.COLLECTION)
        return [cls(**elem) for elem in store_data]  # returns store object or None

    @classmethod
    def get_obj_from_db_by_name(cls, name):
        store_data = Database.find_one(store_constants.COLLECTION,
                                       {'name': name})
        if store_data:
            store_data = cls(**store_data)
        return store_data  # returns store object or None

    @classmethod
    def get_obj_from_db_by_url_prefix(cls, url_prefix):
        store_data = Database.find_one(store_constants.COLLECTION,
                                       {'url_prefix': {'$regex': '^{}'.format(url_prefix)}})
        if store_data:
            store_data = cls(**store_data)
        return store_data  # returns store object or None
        # beginning with url_prefix; use regex to say begins with

    @classmethod
    def get_obj_from_db_by_item_url(cls, item_url):
            split_url = urlsplit(item_url)
            base_url = split_url.scheme + '://' + split_url.hostname
            try:
                store_data = cls.get_obj_from_db_by_url_prefix(base_url)
                return store_data  # returns store object
            except:
                raise store_errors.StoreNotFoundError('Store not found')
            # no store found
            # pass in full item url; use regex to find it

    @staticmethod
    def del_from_db_by_id(_id):
        mydel = Database.delete(store_constants.COLLECTION, {'_id': _id})
        return mydel  # return database record
