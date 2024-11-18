from django.urls import path
from . import views

app_name = 'basket_v2'

urlpatterns = [
    # Show all items in the basket
    path('', views.show_basket, name='show_basket'),

    # Add an item to the basket by its slug
    path(
        'add/<slug:slug>/',
        views.add_to_basket,
        name='add_to_basket'
    ),

    # Remove an item from the basket by its slug
    path(
        'remove/<slug:slug>/',
        views.remove_from_basket,
        name='remove_from_basket'
    ),

    # Clear all items from the basket
    path('clear/', views.clear_basket, name='clear_basket'),
]
