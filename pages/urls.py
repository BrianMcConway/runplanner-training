from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'pages' 

urlpatterns = [
    path('about/', views.about, name='about'),
    path('privacy-policy/', TemplateView.as_view(template_name="pages/privacy_policy.html"), name='privacy_policy'),
    path('terms-of-service/', TemplateView.as_view(template_name="pages/terms_of_service.html"), name='terms_of_service'),
    path('return-policy/', TemplateView.as_view(template_name="pages/return_policy.html"), name='return_policy'),
]