import uuid
import requests
import datetime
from src.common.database import Database
from src.common.utils import Utils
import src.models.alerts.errors as alert_errors
import src.models.alerts.constants as alert_constants
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_obj_from_db_by_id(item_id)
        self.active = active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Alert for {} on item {} with price {}>'.format(self.user_email,
                                                                self.item.name,
                                                                self.price_limit)

    def jsonU(self):
        return {
            "user_email": self.user_email,
            "price_limit": self.price_limit,
            "item_id": self.item._id,
            "active": self.active,
            "last_checked": self.last_checked
        }

    def json(self):
        x = self.jsonU()
        x.update({
            "_id": self._id
        })
        return x

    def save_to_db(self):
        Database.insert(alert_constants.COLLECTION, self.json())

    def update_to_db(self):
        Database.update(alert_constants.COLLECTION, self._id, self.jsonU())

    @staticmethod
    def get_from_db_by_id(_id):
        alert_data = Database.find_one(alert_constants.COLLECTION, {'_id': _id})
        return alert_data  # return database record

    @staticmethod
    def del_from_db_by_id(_id):
        mydel = Database.delete(alert_constants.COLLECTION, {'_id': _id})
        return mydel  # return database record

    @classmethod
    def get_obj_from_db_by_id(cls, _id):
        alert_data = Database.find_one(alert_constants.COLLECTION, {'_id': _id})
        if alert_data:
            alert_data = cls(**alert_data)
        return alert_data  # returns alert object or None

    def send(self):
        mailcode = requests.post(
            alert_constants.MAILGUN_URL,
            auth=('api', alert_constants.MAILGUN_API_KEY),
            data={'from': alert_constants.MAILGUN_FROM,
                  'to': self.user_email,
                  'subject': '{} Price Alert!'.format(self.item.name),
                  'text': "We've found a deal ({})".format(self.item.url)}
        )
        return mailcode

    def deactivate(self):
        self.active = False
        self.update_to_db()

    def activate(self):
        self.active = True
        self.update_to_db()

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        # update alert, then update item database
        self.update_to_db()
        self.item.update_to_db()
        return self.item.price

    @classmethod
    def find_needing_update(cls, minutes_since_update=alert_constants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        db_return = Database.find(alert_constants.COLLECTION, {'last_checked': {'$lte': last_updated_limit}, 'active': True})
#        db_return = Database.find_all('alerts')
#         mylist = []
#         for elem in db_return:
#             print(elem)
#             mylist.append(cls(**elem))
#         return mylist
        return [cls(**elem) for elem in db_return]

    def send_email_if_price_reached(self):
        if float(self.item.price) < float(self.price_limit):
            print('item price is {} trigger price is {}'.format(self.item.price, self.price_limit))
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        db_return = Database.find(alert_constants.COLLECTION, {'user_email': user_email})
        return [cls(**elem) for elem in db_return]
