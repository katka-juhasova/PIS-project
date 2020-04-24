# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Address:
    def __init__(self, street=None, psc=None, city=None, country=None):
        self.street = street.split(',')[0].rstrip() if street else None
        self.house_num = int(street.split(',')[1].rstrip()) if street else None
        self.psc = psc
        self.city = city
        self.country = country


class Customer:
    def __init__(
            self, name=None, surname=None, phone=None, email=None,
            password=None, street=None, psc=None, city=None, country=None
    ):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.password = password
        self.address = Address(street, psc, city, country)
