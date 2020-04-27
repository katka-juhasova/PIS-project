# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .services import Order, Customer, Product
from .services import Product
from .forms import *
from django.contrib import messages
import CIS.models as models
from django.http import HttpResponse

customer = None
order = None


def home(request):
    global order
    global customer
    # if the customer is getting here after hitting button in order details
    # save the order to db
    # if request.method == 'POST':
    #     for key, value in request.POST.items():
    #         if key == 'save order':
    #             new_order = models.Order()
    #             new_order.store_id = order.store_id
    #             new_order.delivery_type = order.delivery_type
    #             new_order.delivery_time_from = order.delivery_time_from
    #             new_order.delivery_time_to = order.delivery_time_to
    #             new_order.courier_id = order.courier_id
    #             new_order.total_price = order.total_price
    #             new_order.total_weight = order.total_weight
    #             new_order.total_amount = order.total_amount
    #             new_order.breakable = order.breakable
    #             new_order.prepared = order.prepared
    #
    #             # if the customer exists just add id
    #             # otherwise create customer record with random password
    #             db_customer = models.Customer.objects.filter(
    #                 email=customer.email)
    #
    #             if len(db_customer) > 0:
    #                 new_order.customer_id = db_customer[0]['id']
    #             else:
    #                 new_address = models.Address()
    #                 new_address.street = customer.address.street
    #                 new_address.psc = customer.address.psc
    #                 new_address.municipality = customer.address.municipality
    #                 new_address.city = customer.address.city
    #                 new_address.save()
    #
    #                 new_customer = models.Customer()
    #                 new_customer.name = customer.name
    #                 new_customer.surname = customer.surname
    #                 new_customer.phone = customer.phone
    #                 new_customer.email = customer.email
    #                 new_customer.address = new_address.id
    #                 new_customer.password = '12345678'
    #                 new_customer.save()
    #
    #                 new_order.customer_id = new_customer.id
    #
    #             new_order.save()
    #
    #             for key, value in order.products.items():
    #                 new_product = models.ProductsInOrder()
    #                 new_product.product_id = key
    #                 new_product.alternative_for = value.alternative_for
    #                 new_product.amount = value.amount
    #                 new_product.available = value.available
    #                 new_product.status = value.status
    #                 new_product.order_id = new_order.id
    #                 new_product.save()
    #
    #             messages.add_message(request, messages.SUCCESS,
    #                                  'Objednávka bola úspešne odoslaná.')

    '''
    NOTE: If you wanna uncomment the upper section comment there 5 lines
    '''
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key == 'save order':
                messages.add_message(request, messages.SUCCESS,
                                     'Objednávka bola úspešne odoslaná.')

    return render(request, 'CIS/home.html')


def my_orders(request):
    return render(request, 'CIS/my_orders.html')


def add_from_catalogue(request):
    global order

    if request.method == 'POST':
        product_id = None
        for key, value in request.POST.items():
            if value == 'Pridať do košíka':
                product_id = key

        db_product = models.Product.objects.filter(id=product_id)
        id_num = product_id
        name = db_product[0].name
        price = db_product[0].price
        weight = db_product[0].weight
        breakable = db_product[0].breakable
        amount = 1
        alternative_for = None
        available = True
        status = 'nepripravený'

        product = Product(id_num=id_num, name=name, price=price, weight=weight,
                          breakable=breakable, amount=amount, status=status,
                          alternative_for=alternative_for, available=available)

        order.add_product(product)

    # just return no content status since no new view needs to be rendered
    return HttpResponse(status=204)


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
                    id=db_customer[0].address_id.id)
                street = db_address[0].street
                psc = db_address[0].psc
                municipality = db_address[0].municipality
                city = db_address[0].city

                customer = Customer(email=email, name=name, surname=surname,
                                    phone=phone, street=street, psc=psc,
                                    municipality=municipality, city=city)

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
        'products': models.Product.objects.all()
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
    global order

    if order is None or order.total_amount == 0:
        return render(request, 'CIS/shopping_cart_empty.html')
    else:
        # if the customer is just changing the amount of products don't render
        # anything and just handle the created changes
        if request.method == 'POST':
            for key, value in request.POST.items():
                if 'plus' in key:
                    product_id = key.replace('plus', '')
                    order.products[product_id].amount += 1
                    order.total_amount += 1
                    order.total_price += order.products[product_id].price
                    order.total_weight += order.products[product_id].weight
                elif 'minus' in key:
                    product_id = key.replace('minus', '')
                    if order.products[product_id].amount == 0:
                        break
                    order.products[product_id].amount -= 1
                    order.total_amount -= 1
                    order.total_price -= order.products[product_id].price
                    order.total_weight -= order.products[product_id].weight

                    # if in any case the customer removed all the products
                    # redirect him to the empty cart
                    if order.total_amount == 0:
                        return render(request, 'CIS/shopping_cart_empty.html')

            return HttpResponse(status=204)

        products_list = list()
        for key, value in order.products.items():
            products_list.append(value)

        context = {
            'products': products_list,
            'total_price': order.total_price
        }

        return render(request, 'CIS/shopping_cart.html', context)


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
            municipality = request.POST['municipality']
            city = request.POST['city']

            # add customer to the order details and move to next window
            customer = Customer(name=name, surname=surname, phone=phone,
                                email=email, street=street, psc=psc,
                                municipality=municipality, city=city)
            order.customer = customer

            return render(request, 'CIS/delivery_settings.html')

    # if the customer is not logged in or nothing happened,just ask him to fill in the form
    return personal_info(request)

def delivery(request):
    return render(request, 'CIS/buy.html')