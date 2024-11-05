from django.urls import path
from . import views, webhooks

app_name = 'checkout_v2'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]
