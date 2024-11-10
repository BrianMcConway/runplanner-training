from django.urls import path
from . import views

app_name = 'my_account'

urlpatterns = [
    path('', views.my_account, name='my_account'),
]
