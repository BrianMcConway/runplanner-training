from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.show_basket, name='show_basket'),
    path('add-to-basket/<str:distance>/<str:difficulty>/<str:terrain>/<str:elevation>/<str:event_date>/', views.add_to_basket, name='add_to_basket'),
    path('remove/<str:item_type>/<str:item_id>/', views.remove_from_basket, name='remove_from_basket'),  # Change int:item_id to str:item_id
    path('empty/', views.empty_basket, name='empty_basket'),
]
