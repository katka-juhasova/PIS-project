# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .services import Order, Customer, Store, Product, Courier
from .services import choose_suitable_store
from .services import order_courier
from .services import checkOrderWeekendTime
from .services import generate_email_text
from .services import replace_products
from .forms import *
from django.contrib import messages
import CIS.models as models
from django.http import HttpResponse
import zeep

customer = None
order = None

def home(request):
    global order
    global customer

    # if the customer is getting here after hitting button in order details
    # save the order to db
    if request.method == 'POST':
        for key, value in request.POST.items():             
            if key == 'save order':
                new_order = models.Order()
                new_order.store_id = order.store_id
                new_order.delivery_type = order.delivery_type
                if order.delivery_type == 'curier':
                    new_order.delivery_time_to = order.delivery_time_to 
                    new_order.delivery_time_from = order.delivery_time_from
                elif order.delivery_type == 'personal collection':
                    new_order.delivery_time_to = "2000-01-01 10:00"
                    new_order.delivery_time_from = "2000-01-01 10:00"
                new_order.total_price = order.total_price
                new_order.total_weight = order.total_weight
                new_order.total_amount = order.total_amount
                new_order.breakable = order.breakable
                new_order.prepared = order.prepared
                
    
                # if the customer exists just add id
                # otherwise create customer record with random password
                db_customer = models.Customer.objects.filter(
                    email=customer.email)
    
                if len(db_customer) > 0:
                    new_order.customer_id = db_customer[0].id
                else:
                    new_address = models.Address()
                    new_address.street = customer.address.street
                    new_address.psc = customer.address.psc
                    new_address.municipality = customer.address.municipality
                    new_address.city = customer.address.city
                    new_address.save()
    
                    new_customer = models.Customer()
                    new_customer.name = customer.name
                    new_customer.surname = customer.surname
                    new_customer.phone = customer.phone
                    new_customer.email = customer.email
                    new_customer.address = new_address.id
                    new_customer.password = '12345678'
                    new_customer.save()
    
                    new_order.customer_id = new_customer.id
    
                new_order.save()
    
                for key, value in order.products.items():
                    new_product = models.ProductsInOrder()
                    new_product.product_id = key
                    new_product.alternative_for = value.alternative_for
                    new_product.amount = value.amount
                    new_product.available = value.available
                    new_product.status = value.status
                    new_product.order_id = new_order.id
                    new_product.save()
    
                messages.add_message(request, messages.SUCCESS,
                                      'Objednávka bola úspešne odoslaná.')
                # send e-mail to the customer
                email_text = generate_email_text(order)
                email_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL'
                email_client = zeep.Client(wsdl=email_wsdl)
                email_client.service.notify(
                    '024', 'NXWZ2Q', customer.email,
                    'Potvrdenie objednávky', email_text
                )
                print(email_text)

   # '''
   # NOTE: If you wanna uncomment the upper section comment there 5 lines
   # '''
    #if request.method == 'POST':
    #    for key, value in request.POST.items():
    #        if key == 'save order':
    #            messages.add_message(request, messages.SUCCESS,
    #                                 'Objednávka bola úspešne odoslaná.')
    #
    #            # send e-mail to the customer
    #            email_text = generate_email_text(order)
    #            email_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/NotificationServices/Email?WSDL'
    #            email_client = zeep.Client(wsdl=email_wsdl)
    #            email_client.service.notify(
    #                '024', 'NXWZ2Q', customer.email,
    #                'Potvrdenie objednávky', email_text
    #            )
    #            print(email_text)
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
        image = db_product[0].image
        amount = 1
        alternative_for = None
        available = True
        status = 'nepripravený'

        product = Product(id_num=id_num, name=name, price=price, weight=weight,
                          breakable=breakable, amount=amount, status=status,
                          alternative_for=alternative_for, available=available, image=image)

        order.add_product(product)
        
    # just return no content status since no new view needs to be rendered
    return HttpResponse(status=204)


# I know, it's totally disgusting view but I'm no expert in django
def catalogue(request):
    global customer
    global order

    # handle potential login from previous site
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        # validate email with WSDL
        validator_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/Validator?WSDL'
        validator_client = zeep.Client(wsdl=validator_wsdl)
        success = validator_client.service.validateEmail(
            request.POST['email'])

        if login_form.is_valid() and success:

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
        'products': models.Product.objects.all(),
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
    if request.method == 'POST' and customer is None:
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

            if order.store_id is None:
                store = choose_suitable_store(order)
                messages.add_message(request, messages.SUCCESS,
                                        'Vaša objednávka bude spracovaná na prevádzke '+ store.city +', ' + store.municipality)

            print("sdas")
            for i in store.missing_products:
                print(i)

            '''
            NOTE FOR DAVID: store.missing_products id list containing id 
            of unavailable products which needs to be replaced by alternatives
            this is the case when the customer is not logged it
            '''

            return render(request, 'CIS/delivery_settings.html')

    # if the customer is not logged in just ask him to fill in the form
    if customer is None:
        return personal_info(request)

    if order.store_id is None:
        store = choose_suitable_store(order)
        messages.add_message(request, messages.SUCCESS,
                                        'Vaša objednávka bude spracovaná na prevádzke '+ store.city +', ' + store.municipality)

    product_num = len(order.products)
    for product in range(1, product_num + 1):
        alternative, alternative_amount, store_amount = replace_products(store.id_num, order.products[str(product)].id_num, order.products[str(product)].amount)
        if alternative is None:
            continue
        order.total_price += (order.products[str(product)].price * store_amount) - (order.products[str(product)].price * order.products[str(product)].amount)
        order.total_weight += (order.products[str(product)].weight * store_amount) - (order.products[str(product)].weight * order.products[str(product)].amount)
        order.total_amount += store_amount - order.products[str(product)].amount
        order.products[str(product)].amount = store_amount
        if store_amount == 0:
            order.products[str(product)].available = False
        if alternative_amount > 0:
            db_product = models.Product.objects.filter(id=alternative)
            id_num = alternative
            name = db_product[0].name
            price = db_product[0].price
            weight = db_product[0].weight
            breakable = db_product[0].breakable
            image = db_product[0].image
            amount = alternative_amount
            alternative_for = product
            available = True
            status = 'nepripravený'

            alternative_product = Product(id_num=id_num, name=name, price=price, weight=weight,
                              breakable=breakable, amount=amount, status=status,
                              alternative_for=alternative_for, available=available, image=image)

            order.add_product(alternative_product)
            order.total_amount += alternative_amount - 1
            order.total_price += db_product[0].price * (alternative_amount - 1)
            order.total_weight += db_product[0].weight * (alternative_amount - 1)


    '''
    NOTE FOR DAVID: store.missing_products id list containing id of unavailable 
    products which needs to be replaced by alternatives
    this is the case when customer is logged in
    '''

    return render(request, 'CIS/delivery_settings.html')


def delivery(request):
    global order

    if "curier" in request.POST:
        checkWeekend = checkOrderWeekendTime(request.POST['casOd'], request.POST['casDo'])
        if checkWeekend:
            messages.add_message(request, messages.ERROR,
                                        'Kuriér počas víkendu nepracuje')
            return render(request, 'CIS/courier_rejected.html')
        else:
            order.delivery_type = 'curier'
            order.delivery_time_from = request.POST['casOd']
            order.delivery_time_to = request.POST['casDo']
            order_courier(order)

            if order.courier_id:
                courier = models.Courier.objects.get(id=order.courier_id)
                store = models.Store.objects.get(id=order.store_id)
                totalPriceForProductType = dict()
                for key, value in order.products.items():
                    totalPriceForProductType[key] = value.amount*value.price
                context = {
                    'products': order.products.items(),
                    'productTypePrice': totalPriceForProductType.items(),
                    'order' : order,
                    'store' : store,
                    'courier': courier
                }
                return render(request, 'CIS/order_details.html', context)
            else:
                messages.add_message(request, messages.ERROR,
                                        'Nepodarilo sa nájsť vhodného kuriéra')
                return render(request, 'CIS/courier_rejected.html')
    else:
        store = models.Store.objects.get(id=order.store_id)
        totalPriceForProductType = dict()
        for key, value in order.products.items():
            totalPriceForProductType[key] = value.amount*value.price
        order.delivery_type = 'personal collection'
        context = {
                'products': order.products.items(),
                'productTypePrice': totalPriceForProductType.items(),
                'order' : order,
                'store' : store,
            }
        return render(request, 'CIS/order_details.html', context)
