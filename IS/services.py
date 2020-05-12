# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from decimal import *
import zeep
import sqlite3
import CIS.models as models
import operator
import requests
import json

class Address:
    def __init__(self, street=None, psc=None, municipality=None, city=None):
        self.street = street.split(',')[0].rstrip() if street else None
        self.house_num = int(street.split(',')[1].rstrip()) if street else None
        self.psc = psc
        self.municipality = municipality
        self.city = city


class Customer:
    def __init__(
            self, name=None, surname=None, phone=None, email=None,
            street=None, psc=None, municipality=None, city=None
    ):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.address = Address(street, psc, municipality, city)

class Order:
    def __init__(self, customer: Customer):
        getcontext().prec = 28
        self.customer = customer
        self.products = dict()  # key = id of the product, value = product obj
        self.store_id = None
        self.delivery_type = None
        self.delivery_time_from = None
        self.delivery_time_to = None
        self.courier_id = None
        self.total_price = Decimal('0')
        self.total_weight = Decimal('0')
        self.total_amount = 0
        self.breakable = False
        self.prepared = False

class ProductsInOrder:
    def __init__(self, id_num: int, name: str, price: float, weight: float,
                 breakable: bool, amount: int, available: bool, status: str, image: str,
                 alternative_for: int or None, alternative_for_name: str or None, 
                 alternative_for_image: str or None, alternative_for_price: float or None):
        self.id_num = id_num
        self.name = name
        self.price = price
        self.weight = weight
        self.breakable = breakable
        self.amount = amount
        self.available = available
        self.status = status
        self.image = image
        self.alternative_for = alternative_for
        self.alternative_for_name = alternative_for_name
        self.alternative_for_image = alternative_for_image
        self.alternative_for_price = alternative_for_price
        