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