from django.urls import path
from . import views

app_name = 'my_account'

urlpatterns = [
    path('', views.my_account, name='my_account'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/purchased-plans/', views.purchased_plans, name='purchased_plans'),
    path('profile/purchased-plans/training-plan/<int:id>/', views.view_training_plan, name='view_training_plan'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
]