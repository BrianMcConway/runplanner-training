from django.urls import path
from . import views

urlpatterns = [
    path('training-plans/', views.training_plans, name='training_plans'),
]
