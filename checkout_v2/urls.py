from django.urls import path
from . import views, webhooks

app_name = 'checkout_v2'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
    path('check_order_payment/<int:order_id>/', views.check_order_payment, name='check_order_payment'),
]