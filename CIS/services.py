# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from decimal import *


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


class Product:
    def __init__(self, id_num: int, name: str, price: float, weight: float,
                 breakable: bool, amount: int, alternative_for: int or None,
                 available: bool, status: str):
        self.id_num = id_num
        self.name = name
        self.price = price
        self.weight = weight
        self.breakable = breakable
        self.amount = amount
        self.alternative_for = alternative_for
        self.available = available
        self.status = status


class Order:
    def __init__(self, customer: Customer):
        getcontext().prec = 28
        self.customer = customer
        self.products = dict()
        self.store = None
        self.delivery_type = None
        self.delivery_time_from = None
        self.delivery_time_to = None
        self.courier = None
        self.total_price = Decimal('0')
        self.total_weight = Decimal('0')
        self.total_amount = 0
        self.breakable = False
        self.prepared = False

    def add_product(self, product: Product):
        self.products[product.id_num] = product
        self.total_amount += 1
        self.total_price += product.price
        self.total_weight += product.weight
        self.breakable = (self.breakable or product.breakable)

    def increase_product_amount(self, product_id: int, amount: int):
        diff = amount - self.products[product_id].amount
        self.products[product_id].amount = amount
        self.total_amount += diff
        self.total_price += diff * self.products[product_id].price
        self.total_weight += diff * self.products[product_id].weight

    def determine_vehicle(self) -> str:
        if self.breakable or self.total_amount > 10 or self.total_weight > 20.:
            return 'automobile'

        return 'bicycle'
