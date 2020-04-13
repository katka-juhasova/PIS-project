# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, 'CIS/home.html')


def my_orders(request):
    return render(request, 'CIS/my_orders.html')


def catalogue(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'CIS/catalogue.html', context)


def login(request):
    return render(request, 'CIS/login.html')


def order_details(request):
    return render(request, 'CIS/order_details.html')


def alternatives(request):
    return render(request, 'CIS/alternatives.html')


def shopping_cart_empty(request):
    return render(request, 'CIS/shopping_cart_empty.html')


def shopping_cart(request):
    return render(request, 'CIS/shopping_cart.html')


def courier_rejected(request):
    return render(request, 'CIS/courier_rejected.html')


def personal_info(request):
    return render(request, 'CIS/personal_info.html')

