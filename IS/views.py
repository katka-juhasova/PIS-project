from django.shortcuts import render
from .forms import *
import CIS.models as models
from django.contrib import messages
from .services import Customer, Order, ProductsInOrder
import zeep
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

customer = None
order = None
orderId = None
user = None

def home(request):
    global order
    global customer
    return render(request, 'IS/home.html')

def login(request):
    return render(request, 'IS/login.html')

def order_detail(request, order_id):
    global orderId
    global user

    orderId = order_id
    
    order = models.Order.objects.get(id=order_id)
    store = models.Store.objects.get(id=order.store_id)
    customer = models.Customer.objects.get(id=order.customer_id)
    products = []
    productsFromOrder = models.ProductsInOrder.objects.filter(order=order_id)
    
    for product in productsFromOrder:
        productTemp = models.Product.objects.get(id=product.product_id)
        if product.alternative_for is not None:
            productAlternative = models.Product.objects.get(id=product.alternative_for)
            productListTemp = ProductsInOrder(productTemp.id, productTemp.name, productTemp.price, productTemp.weight, 
                        productTemp.breakable, product.amount, product.available, product.status, productTemp.image,
                        product.alternative_for, productAlternative.name, productAlternative.image, productAlternative.price)
        else:
            productListTemp = ProductsInOrder(productTemp.id, productTemp.name, productTemp.price, productTemp.weight, 
                        productTemp.breakable, product.amount, product.available, product.status, productTemp.image, None, None, None, None)
        products.append(productListTemp)
    
    context = {
        'products': products,
        'order': order,
        'store' : store,
        'customer': customer,
        'user' : user,
    }

    if order.courier_id is not None:
        curier = models.Courier.objects.get(id=order.courier_id)
        context = {
            'products': products,
            'order': order,
            'store' : store,
            'customer': customer,
            'curier' : curier,
            'user' : user,
        }

    return render(request, 'IS/order_detail.html', context)

def orders(request):
    global customer
    global order
    global orderId
    global user

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key == 'save order':
                if 'status' in request.POST:
                    status = request.POST['status']
                    models.ProductsInOrder.objects.filter(order = orderId).update(status = status)
                    if user.email == 'pokladnik@gmail.com':
                        models.Order.objects.filter(id=orderId).update(prepared=True)    
                    
                    orders = []
                    # load products to be shown in catalogue
                    if user.email == 'pokladnik@gmail.com':
                        productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='pripravený').values('order').distinct()
                        for productInOrderWhichIsReady in productsInOrderWhichAreReady:
                            orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
                            if orderTemp.prepared == False:
                                orders.append(orderTemp)
                    elif user.email == 'skladnik@gmail.com':
                        productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='nepripravený').values('order').distinct()
                        for productInOrderWhichIsReady in productsInOrderWhichAreReady:
                            orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
                            orders.append(orderTemp)
                    
                    paginator = Paginator(orders, 5)
                    page = request.GET.get('page')
                    orders = paginator.get_page(page)

                    context = {
                        'orders' : orders,
                    }

                    return render(request, 'IS/orders.html', context)

    # handle potential login from previous site
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        # validate email with WSDL
        validator_wsdl = 'http://pis.predmety.fiit.stuba.sk/pis/ws/Validator?WSDL'
        validator_client = zeep.Client(wsdl=validator_wsdl)
        success = validator_client.service.validateEmail(
            request.POST['email'])

        if login_form.is_valid() and success:

            db_customer = models.Customer.objects.get(email=request.POST['email'])
            print(db_customer.email)
            user = db_customer

            # if we got here, we have read our customer details from db
            # and we'll send message about successful login to the catalogue
            if db_customer.email == 'skladnik@gmail.com':
                messages.add_message(request, messages.SUCCESS,
                                 'Boli ste úspešne prihlásený ako skladník.')
                # load products to be shown in catalogue
                orders = []
                productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='nepripravený').values('order').distinct()
                for productInOrderWhichIsReady in productsInOrderWhichAreReady:
                    orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
                    orders.append(orderTemp)    
                paginator = Paginator(orders, 5)
                page = request.GET.get('page')
                orders = paginator.get_page(page)

                context = {
                    'orders' : orders,
                }

                return render(request, 'IS/orders.html', context)


            elif db_customer.email == 'pokladnik@gmail.com':
                messages.add_message(request, messages.SUCCESS,
                                 'Boli ste úspešne prihlásený ako pokladník.')
                # load products to be shown in catalogue
                orders = []
                productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='pripravený').values('order').distinct()
                for productInOrderWhichIsReady in productsInOrderWhichAreReady:
                    orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
                    if orderTemp.prepared == False:
                        orders.append(orderTemp)    
                paginator = Paginator(orders, 5)
                page = request.GET.get('page')
                orders = paginator.get_page(page)

                context = {
                    'orders' : orders,
                }

                return render(request, 'IS/orders.html', context)
            else:
                messages.add_message(request, messages.ERROR,
                                     'Nesprávny e-mail alebo heslo.')
                context = {
                    'email': request.POST['email'],
                    'password': request.POST['password']
                }
                return render(request, 'IS/login.html', context=context)

    orders = []
    # load products to be shown in catalogue
    if user.email == 'pokladnik@gmail.com':
        productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='pripravený').values('order').distinct()
        for productInOrderWhichIsReady in productsInOrderWhichAreReady:
            orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
            if orderTemp.prepared == False:
                orders.append(orderTemp)
    elif user.email == 'skladnik@gmail.com':
        productsInOrderWhichAreReady = models.ProductsInOrder.objects.filter(status='nepripravený').values('order').distinct()
        for productInOrderWhichIsReady in productsInOrderWhichAreReady:
            orderTemp = models.Order.objects.get(id=productInOrderWhichIsReady['order'])
            orders.append(orderTemp)

    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    context = {
        'orders' : orders,
    }

    return render(request, 'IS/orders.html', context)
