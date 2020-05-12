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

def home(request):
    global order
    global customer
    return render(request, 'IS/home.html')

def login(request):
    return render(request, 'IS/login.html')

def order_detail(request, order_id):
    global orderId
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
    }

    if order.courier_id is not None:
        curier = models.Courier.objects.get(id=order.courier_id)
        context = {
            'products': products,
            'order': order,
            'store' : store,
            'customer': customer,
            'curier' : curier
        }

    return render(request, 'IS/order_detail.html', context)

def orders(request):
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

            # if there's no customer found print error and let the customer
            # try to log in again
            if db_customer is None:
                messages.add_message(request, messages.ERROR,
                                     'Nesprávny e-mail alebo heslo.')
                context = {
                    'email': request.POST['email'],
                    'password': request.POST['password']
                }
                return render(request, 'IS/login.html', context=context)

            # if we got here, we have read our customer details from db
            # and we'll send message about successful login to the catalogue
            messages.add_message(request, messages.SUCCESS,
                                 'Boli ste úspešne prihlásený.')

    # load products to be shown in catalogue
    orders = models.Order.objects.all()

    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    context = {
        'orders' : orders,
        'products': models.ProductsInOrder.objects.all()
    }

    return render(request, 'IS/orders.html', context)
