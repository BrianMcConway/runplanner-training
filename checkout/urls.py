from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout_view'),  # Checkout page URL
    path('success/', views.payment_success, name='payment_success'),  # Change to 'success/' if that's your desired path
    path('error/', views.payment_error, name='payment_error'),
]
