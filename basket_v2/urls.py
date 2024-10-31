from django.urls import path
from . import views

app_name = 'basket_v2'

urlpatterns = [
    path('', views.show_basket, name='show_basket'),
    path('add/<slug:slug>/', views.add_to_basket, name='add_to_basket'),
    path('remove/<slug:slug>/', views.remove_from_basket, name='remove_from_basket'),
    path('clear/', views.clear_basket, name='clear_basket'),
]
