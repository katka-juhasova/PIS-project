from django.shortcuts import render
from .forms import *
import CIS.models as models
from django.contrib import messages
from .services import Customer, Order
import zeep
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

customer = None
order = None


def home(request):
    global order
    global customer
    return render(request, 'IS/home.html')

def login(request):
    return render(request, 'IS/login.html')

def order_detail(request):
    return render(request, 'IS/order_detail.html')

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
