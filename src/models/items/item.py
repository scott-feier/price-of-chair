import uuid
import requests
import datetime
from bs4 import BeautifulSoup
import re
from src.common.database import Database
from src.common.utils import Utils
import src.models.items.errors as item_errors
import src.models.items.constants as item_constants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, created_date=None, _id=None):
        self.name = name
        self.url = url
        self.price = None if price is None else price
        self.created_date = datetime.datetime.utcnow().isoformat() if created_date is None else created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Alert for item {} at url {}>'.format(self.name,
                                                      self.url)

    def jsonU(self):
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "created_date": self.created_date
        }

    def json(self):
        x = self.jsonU()
        x.update({
            "_id": self._id
        })
        return x

    def load_price(self):
        store = Store.get_obj_from_db_by_item_url(self.url)  # store object
        tag_name = store.tag_name
        query = store.query

        request = requests.get(self.url)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

#        Amazon pattern - string_price = soup.find("span", {"id": "priceblock_ourprice"}).text.strip()

        string_price = soup.find(tag_name, query)
        if string_price is None:
            return None
        else:
            string_price = string_price.text.strip()

        num_price = string_price.replace(',', '')  # replace any commas
        pattern = re.compile('(\d+.\d+)')
        match = pattern.search(num_price)

        string_price = match.group()  # string price stripped of currency and commas
        self.price = string_price
        return self.price

        # at this point, you have:
        # string_price - with dollar sign and comma, and if more than one
        #   than all are there
        # num_price - float representation
        # self.price - string stripped of dollar and comma

    def save_to_db(self):
        Database.insert(item_constants.COLLECTION, self.json())

    def update_to_db(self):
        Database.update(item_constants.COLLECTION, self._id, self.jsonU())

    @staticmethod
    def get_from_db_by_id(item_id):
        item_data = Database.find_one(item_constants.COLLECTION, {'_id': item_id})
        return item_data

    @classmethod
    def get_obj_from_db_by_id(cls, item_id):
        item_data = Database.find_one(item_constants.COLLECTION, {'_id': item_id})
        if item_data:
            item_data = cls(**item_data)
        return item_data  # returns item object or None
