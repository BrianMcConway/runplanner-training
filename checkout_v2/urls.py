# checkout_v2/urls.py
from django.urls import path
from . import views

app_name = 'checkout_v2'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Define the main checkout page view
    path('create_order/', views.create_order, name='create_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
]
