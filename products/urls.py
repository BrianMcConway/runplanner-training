from django.urls import path
from . import views

urlpatterns = [
    path('training-plans/', views.training_plans, name='training_plans'),
    path('generate-image/<str:distance>/<str:difficulty>/<str:terrain>/<str:elevation>/<str:event_date>/', views.generate_plan_image, name='generate_plan_image'),
    path('basket/<str:distance>/<str:difficulty>/<str:terrain>/<str:elevation>/<str:event_date>/', views.basket, name='basket'),
]
