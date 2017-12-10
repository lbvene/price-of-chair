from bs4 import BeautifulSoup
import requests
import re
from common.database import Database
from models.stores.store import Store
import models.items.constants as ItemConstants
import uuid

__author__ = 'lbvene'

class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        #self.store = store
        store = Store.get_by_url(url)
        #tag_name = store.get_tag_name()
        #query = store.get_query()
        #tag_name = store.tag_name
        #query = store.query
        self.tag_name = store.tag_name
        self.query = store.query
        #self.price = self.load_price(tag_name, query)
        #self.price = None
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # {"id": "priceblock_ourprice", "class": "a-size-medium a-color-price"}
        #request = requests.get("https://www.amazon.com/Nikon-D750-FX-format-Digital-Camera/dp/B0060MVJ1Q/ref=sr_1_1_sspa?s=photo&ie=UTF8&qid=1512405816&sr=1-1-spons&keywords=camera&psc=1")
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        #element = soup.find(tag_name, query)
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        #price_without_symbol = string_price[1:]
        #price = float(price_without_symbol)
        # parentheses are for group of digits
        pattern = re.compile("(\d+.\d+)") #$115.00
        match = pattern.search(string_price)

        #self.price = match.group()
        # this returns price, which we are then going to put in self.price in __init__
        self.price = float(match.group())
        #return match.group()
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
