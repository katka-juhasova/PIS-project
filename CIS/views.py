# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Product
from .services import Order, Customer
from .forms import *
from django.contrib import messages
import CIS.models as models


customer = None
order = None


def home(request):
    return render(request, 'CIS/home.html')


def my_orders(request):
    return render(request, 'CIS/my_orders.html')


# I know, it's totally disgusting view but I'm no expert in django
def catalogue(request):
    global customer
    global order
    customer = None
    order = None

    # handle potential login from previous site
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            db_customer = models.Customer.objects.filter(
                email=request.POST['email'], password=request.POST['password'])

            # if there's record about our guy in db just load it into customer
            if len(db_customer) == 1:
                name = db_customer[0].name
                surname = db_customer[0].surname
                phone = db_customer[0].phone
                email = db_customer[0].email
                db_address = models.Address.objects.filter(
                    id=db_customer[0].address_id)
                street = db_address[0].street
                psc = db_address[0].psc
                city = db_address[0].city
                country = db_address[0].country

                customer = Customer(email=email, name=name, surname=surname,
                                    phone=phone, street=street, psc=psc,
                                    city=city, country=country)

            # if there's no customer found print error and let the customer
            # try to log in again
            if customer is None:
                messages.add_message(request, messages.ERROR,
                                     'Nesprávny e-mail alebo heslo.')
                context = {
                    'email': request.POST['email'],
                    'password': request.POST['password']
                }
                return render(request, 'CIS/login.html', context=context)

            # if we got here, we have read our customer details from db
            # and we'll send message about successful login to the catalogue
            messages.add_message(request, messages.SUCCESS,
                                 'Boli ste úspešne prihlásený.')

    # handle adding new product

    # init new empty order
    order = Order(customer)
    # load products to be shown in catalogue
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
    # global order
    #
    # if order is None or order.total_amount == 0:
    #     return render(request, 'CIS/shopping_cart_empty.html')
    # else:
    #     return render(request, 'CIS/shopping_cart.html')

    return render(request, 'CIS/shopping_cart.html')


def courier_rejected(request):
    return render(request, 'CIS/courier_rejected.html')


def personal_info(request):
    return render(request, 'CIS/personal_info.html')


def settings(request):
    global customer
    global order

    # handle creating new customer
    if request.method == 'POST':
        personal_info_form = PersonalInfoForm(request.POST)
        if personal_info_form.is_valid():
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            phone = request.POST['phone']
            street = request.POST['street']
            psc = request.POST['psc']
            city = request.POST['city']
            country = request.POST['country']

            # add customer to the order details and move to next window
            customer = Customer(name=name, surname=surname, phone=phone,
                                email=email, street=street, psc=psc, city=city,
                                country=country)
            order.customer = customer

            return render(request, 'CIS/delivery_settings.html')

    # if the customer is not logged in just ask him to fill in the form
    if customer is None:
        return personal_info(request)

    return render(request, 'CIS/delivery_settings.html')

