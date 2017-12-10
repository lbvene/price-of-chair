import uuid
import datetime
import requests
import models.alerts.constants as AlertConstants
from models.items.item import Item
from common.database import Database
import config

__author__ = 'lbvene'

class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        #self.user = user
        self.user_email = user_email
        self.price_limit = price_limit
        #self.item = item
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}.".format(self.item.name),
                "text": "We have found a deal! Click on the link below:\n\n{}\n\nTo navigate to the alert, visit:\n\n{}".format(
                        self.item.url, config.DOMAIN + "/alerts/{}".format(self._id))
            }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        print("Last updated time: {}".format(last_updated_limit))
        print("Minutes since update update time: {}".format(last_updated_limit))
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                        {"last_checked":
                                                            {"$lte": last_updated_limit},
                                                        "active": True
                                                        })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            #"user": self.user.json(),
            "user_email": self.user_email,
            #"item": self.item.json()
            "item_id": self.item._id,
            "active": self.active
        }

    def load_and_save_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price <= self.price_limit:
            print('Email is being sent!')
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email": user_email})]

    # alert_id is unique
    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {"_id": self._id})
