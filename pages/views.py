from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def about(request):
    return render(request, 'pages/about.html')

def test_email(request):
    try:
        send_mail(
            'Test Email Subject',  # Subject
            'This is a test email body.',  # Message
            'brianbioenergy@gmail.com',  # From email
            ['brianmcconway@yahoo.co.uk'],  # To email(s)
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully! Check your console.")
    except Exception as e:
        return HttpResponse(f"Email failed: {e}")