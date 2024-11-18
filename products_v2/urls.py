from django.urls import path
from . import views

app_name = 'products_v2'

urlpatterns = [
    path('', views.training_plans, name='training_plans'),

]
