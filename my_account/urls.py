from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    my_account,
    profile,
    edit_profile,
    purchased_plans,
    view_training_plan,
    delete_account,
)

app_name = 'my_account'

urlpatterns = [
    path('', my_account, name='my_account'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path(
        'profile/purchased-plans/',
        purchased_plans,
        name='purchased_plans',
    ),
    path(
        'profile/purchased-plans/training-plan/<int:id>/',
        view_training_plan,
        name='view_training_plan',
    ),
    path(
        'profile/delete-account/',
        delete_account,
        name='delete_account',
    ),
]
