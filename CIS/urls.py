from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('add_from_catalogue/', views.add_from_catalogue,
         name='add_from_catalogue'),
    path('login/', views.login, name='login'),
    path('order_details/', views.order_details, name='order_details'),
    path('alternatives/', views.alternatives, name='alternatives'),
    path('shopping_cart_empty/', views.shopping_cart_empty,
         name='shopping_cart_empty'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('courier_rejected/', views.courier_rejected, name='courier_rejected'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('settings/', views.settings, name='settings'),
]
