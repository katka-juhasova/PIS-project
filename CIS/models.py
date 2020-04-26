# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=100)
    psc = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    weight = models.DecimalField(decimal_places=2, max_digits=10)
    breakable = models.BooleanField()
    image = models.CharField(max_length=100)


class Store(models.Model):
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)


class ProductsInStore(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)


class Courier(models.Model):
    name = models.CharField(max_length=100)
    automobile = models.BooleanField()
    bicycle = models.BooleanField()


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=20)
    delivery_time_from = models.DateTimeField()
    delivery_time_to = models.DateTimeField()
    courier_id = models.ForeignKey(Courier, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    total_weight = models.IntegerField()
    total_amount = models.IntegerField()
    breakable = models.BooleanField()
    prepared = models.BooleanField()


class ProductsInOrder(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    # alternative_for = models.ForeignKey(Product, on_delete=models.CASCADE)
    # nejde mat 2 foreign keys do tej istej table, povedzme, ze tu bude len id alternativy
    alternative_for = models.IntegerField()
    amount = models.IntegerField()
    available = models.BooleanField()
    status = models.CharField(default='nepripravený', max_length=20)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)


class Notification(models.Model):
    type = models.CharField(max_length=10)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)





