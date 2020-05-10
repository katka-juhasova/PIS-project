from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('add_from_catalogue/', views.add_from_catalogue,
         name='add_from_catalogue'),
    path('login/', views.login, name='login'),
    path('log/', views.log, name='log'),
    path('order_details/', views.order_details, name='order_details'),
    path('alternatives/', views.alternatives, name='alternatives'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('shopping_cart_empty/', views.shopping_cart_empty,
         name='shopping_cart_empty'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('courier_rejected/', views.courier_rejected, name='courier_rejected'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('settings/', views.settings, name='settings'),
    path('delivery/', views.delivery, name='delivery'),
    path('order/', views.order, name='order'),
    path('remove_product/', views.remove_product, name='remove_product'),
]
