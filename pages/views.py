from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def about(request):
    return render(request, 'pages/about.html')

from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /checkout/",
        "Disallow: /basket/",
        "Sitemap: https://runplanner-training-cfec4c16a60a.herokuapp.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")