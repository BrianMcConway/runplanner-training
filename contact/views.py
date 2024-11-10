from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse  # to get URL for redirecting
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact:success')  # Redirect to a new success page
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact_form.html', {'form': form})

def success_view(request):
    return render(request, 'contact/success.html')