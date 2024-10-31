from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Home page with no namespace as it's the main entry
]
