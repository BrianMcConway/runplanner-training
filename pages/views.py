from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def about(request):
    return render(request, 'pages/about.html')
