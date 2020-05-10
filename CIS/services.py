# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from decimal import *
import zeep
import sqlite3
import CIS.models as models
from CIS.sql_queries import SQLITE_SELECT_MUNICIPALITY
from CIS.sql_queries import SQLITE_SELECT_CITY
from CIS.sql_queries import SQLITE_SELECT_ALL_STORES
from CIS.sql_queries import SQLITE_SELECT_PRODUCTS_IN_STORE
from CIS.sql_queries import SQLITE_SELECT_COURIER_ID
from CIS.sql_queries import SQLITE_SELECT_COURIER_AUTOMOBILE
from CIS.sql_queries import SQLITE_SELECT_COURIER_BICYCLE
from CIS.sql_queries import SQLITE_MISSING
from CIS.sql_queries import SQLITE_ALTERNATIVE
from CIS.sql_queries import SQLITE_ORDERS
from CIS.sql_queries import SQLITE_PRODUCTS
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


class Product:
    def __init__(self, id_num: int, name: str, price: float, weight: float,
                 breakable: bool, amount: int, alternative_for: int or None,
                 available: bool, status: str, image: str):
        self.id_num = id_num
        self.name = name
        self.price = price
        self.weight = weight
        self.breakable = breakable
        self.amount = amount
        self.alternative_for = alternative_for
        self.available = available
        self.status = status
        self.image = image


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


class MissingProduct:
    def __init__(self, id_num: int, amount: int):
        self.id_num = id_num
        self.amount = amount


class Store:
    def __init__(self, id_num: int, municipality: str, city: str):
        self.id_num = id_num
        self.municipality = municipality
        self.city = city
        self.latitude = 0.
        self.longitude = 0.
        self.distance = 0.
        # list of products from order, which are unavailable in store
        self.missing_products = list()


class Courier:
    def __init__(self, id_num: int):
        self.id_num = id_num
        self.automobile = False
        self.bicycle = False


'''
BP Výber prevádzky
writes store id into Order attribute "store_id" 
and returns Store object, which includes (besides other attributes) id number 
(id_num) of the chosen store and list of id numbers of missing products which 
are listed in the order but not available in chosen store (missing_products)
'''


def choose_suitable_store(order: Order):
    municipalities_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Municipalities?WSDL'
    municipalities_client = zeep.Client(wsdl=municipalities_wsdl)

    locations_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/GeoServices/Locations?WSDL'
    locations_client = zeep.Client(wsdl=locations_wsdl)

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    customer_municipality = order.customer.address.municipality
    customer_city = order.customer.address.city
    if customer_city != customer_municipality:
        customer_address = municipalities_client.service.getByName(
            '{} - {}'.format(customer_city, customer_municipality))
    else:
        customer_address = municipalities_client.service.getByName(
            customer_municipality)

    # first select all stores from db and assign corresponding GPS coords
    # and count the distance from customer
    stores = list()
    cursor.execute(SQLITE_SELECT_ALL_STORES)
    db_stores = cursor.fetchall()

    for store in db_stores:
        cursor.execute(SQLITE_SELECT_MUNICIPALITY, (store[0],))
        db_municipality = cursor.fetchall()
        cursor.execute(SQLITE_SELECT_CITY, (store[0],))
        db_city = cursor.fetchall()
        stores.append(Store(store[0],
                            municipality=db_municipality[0][0],
                            city=db_city[0][0]))

    for i, store in enumerate(stores):
        if store.city != store.municipality:
            municipality = municipalities_client.service.getByName(
                '{} - {}'.format(store.city, store.municipality)
            )

        else:
            municipality = municipalities_client.service.getByName(store.city)

        stores[i].latitude = municipality['coord_lat']
        stores[i].longitude = municipality['coord_lon']
        stores[i].distance = locations_client.service.distanceByGPS(
            stores[i].latitude, stores[i].longitude,
            customer_address['coord_lat'], customer_address['coord_lon']
        ) / 1000.

    for i, store in enumerate(stores):
        cursor.execute(SQLITE_SELECT_PRODUCTS_IN_STORE, (store.id_num,))
        db_store_products = cursor.fetchall()
        store_products = list()
        for product in db_store_products:
            store_products.append(product[0])

        for product in order.products:
            if int(product) not in store_products:
                stores[i].missing_products.append(product)

    # sort stores according to the distance
    sorted_stores = sorted(stores, key=operator.attrgetter('distance'))

    # choose the best store
    for store in sorted_stores:
        if store.distance < 100. and len(store.missing_products) == 0:
            order.store_id = store.id_num
            return store

        if store.distance > 100.:
            order.store_id = sorted_stores[0].id_num
            return sorted_stores[0]


# BP Výber vozidla
def choose_vehicle(order: Order) -> str:
    if order.breakable or order.total_amount > 10 or order.total_weight > 20.:
        return 'automobile'

    return 'bicycle'


'''
running this function with order parameter would add courier id 
to order.courier_id if the courier was successfully found, otherwise the value 
of courier_id shall remain None 
NOTE: API must be running on http://127.0.0.1:5000/ when using this function
'''


# BP Objednanie kuriérae
def order_courier(order: Order):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(SQLITE_SELECT_COURIER_ID)
    db_couriers = cursor.fetchall()

    couriers = list()
    for courier in db_couriers:
        couriers.append(Courier(id_num=courier[0]))

    for i, courier in enumerate(couriers):
        cursor.execute(SQLITE_SELECT_COURIER_AUTOMOBILE, (courier.id_num,))
        automobile = cursor.fetchall()
        couriers[i].automobile = bool(automobile[0][0])

        cursor.execute(SQLITE_SELECT_COURIER_BICYCLE, (courier.id_num,))
        bicycle = cursor.fetchall()
        couriers[i].bicycle = bool(bicycle[0][0])

    vehicle = choose_vehicle(order)
    api_url_base = 'http://127.0.0.1:5000/courier/'
    for courier in couriers:
        if vehicle == 'automobile':
            if courier.automobile:
                api_url = '{}{}'.format(api_url_base, courier.id_num)
                response = requests.get(api_url)
                success = json.loads(
                    response.content.decode('utf-8'))['success']
                if success:
                    order.courier_id = courier.id_num
                    return

        else:
            if courier.bicycle:
                api_url = '{}{}'.format(api_url_base, courier.id_num)
                response = requests.get(api_url)
                success = json.loads(
                    response.content.decode('utf-8'))['success']
                if success:
                    order.courier_id = courier.id_num
                    return

def checkOrderWeekendTime(deliveryFrom: str, deliveryTo: str):
    calendar_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/Calendar?WSDL'
    calendar_client = zeep.Client(wsdl=calendar_wsdl)

    check_delivery_time_from = calendar_client.service.isWeekend(deliveryFrom.split(' ')[0])
    check_delivery_time_to = calendar_client.service.isWeekend(deliveryTo.split(' ')[0])
    
    if check_delivery_time_from or check_delivery_time_to:
        return True
    else:
        return False


def generate_email_text(order: Order):
    message = 'Vážený zákazník ' + order.customer.name + ', Vaša objednávka bola spracovaná.\n Obsah objednávky: '
    for key, value in order.products.items():
        message += value.name + ', '
    message += 'celková cena: ' + str(order.total_price) + '€. '
    store = models.Store.objects.get(id=order.store_id)
    if order.delivery_type == 'curier':
        courier = models.Courier.objects.get(id=order.courier_id)                
        message += 'Spôsob doručenia: Kuriér ,' + courier.name + '.\nZvolený čas doručenia: ' + order.delivery_time_from + ' - ' + order.delivery_time_to + '.\nPrevádzka: ' + store.address.city + ', ' + store.address.street + '.'
    elif order.delivery_type == 'personal collection':
        message += 'Spôsob doručenia: Osobný odber.\n Prevádzka: ' + store.address.city + ', ' + store.address.street + '.'
    message += ' Ďakujeme za Vašu objednávku.'
    return message


def replace_products(store, product, amount):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(SQLITE_MISSING, (store, product))
    store_amount = cursor.fetchall()
    if store_amount[0][0] >= amount:
        return None, None, None
    cursor.execute(SQLITE_ALTERNATIVE, product)
    alternative = cursor.fetchall()
    cursor.execute(SQLITE_MISSING, (store, str(alternative[0][0])))
    alternative_amount = cursor.fetchall()
    if alternative_amount.__len__() == 0:
        alternative_amounts = 0
    else:
        alternative_amounts = alternative_amount[0][0]
    missing_amount = amount - store_amount[0][0]
    if missing_amount <= alternative_amounts:
        return alternative[0][0], missing_amount, store_amount[0][0]
    return alternative[0][0], alternative_amounts, store_amount[0][0]


def load_orders(customer):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(SQLITE_ORDERS, str(customer))
    orders = cursor.fetchall()
    return orders


def load_products(order):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(SQLITE_PRODUCTS, str(order))
    order = cursor.fetchall()
    return order


# this main is just for testing the functionality of the functions
if __name__ == '__main__':
    o = Order(Customer(municipality='Ružinov', city='Bratislava'))
    o.products['1'] = Product(id_num=1, name='', price=0., weight=0.,
                              breakable=False, amount=1, available=True,
                              status='', alternative_for=None)
    o.products['2'] = Product(id_num=2, name='', price=0., weight=0.,
                              breakable=False, amount=1, available=True,
                              status='', alternative_for=None)
    o.products['3'] = Product(id_num=3, name='', price=0., weight=0.,
                              breakable=False, amount=1, available=True,
                              status='', alternative_for=None)
    o.products['4'] = Product(id_num=4, name='', price=0., weight=0.,
                              breakable=False, amount=1, available=True,
                              status='', alternative_for=None)
    o.products['5'] = Product(id_num=5, name='', price=0., weight=0.,
                              breakable=False, amount=1, available=True,
                              status='', alternative_for=None)

    o.total_weight = 50.5
    order_courier(o)
    print(o.courier_id)
