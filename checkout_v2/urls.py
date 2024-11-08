from django.urls import path
from . import views, webhooks

app_name = 'checkout_v2'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]
