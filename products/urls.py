from django.urls import path
from . import views

urlpatterns = [
    path('training-plans/', views.training_plans, name='training_plans'),
    path('basket/', views.basket, name='basket'),
    path('add-to-basket/<str:distance>/<str:difficulty>/<str:terrain>/<str:elevation>/<str:event_date>/', views.add_to_basket, name='add_to_basket'),
    path('remove-from-basket/', views.remove_from_basket, name='remove_from_basket'),  # URL for removing items from basket
]
