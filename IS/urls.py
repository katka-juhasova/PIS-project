from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='homeIS'),
    path('login/', views.login, name='login'),
    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
]
