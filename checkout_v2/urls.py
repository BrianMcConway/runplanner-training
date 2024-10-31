from django.urls import path
from . import views

app_name = 'checkout_v2'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),  # Single checkout view handles everything
]
