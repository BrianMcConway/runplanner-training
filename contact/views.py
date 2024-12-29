from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse  # To get URL for redirecting
from .forms import ContactForm


def contact_view(request):
    """
    Handles the contact form submission. Displays the contact form
    and processes the form data when submitted.
    """
    if request.method == 'POST':
        # Populate the form with POST data
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Display a success message to the user
            messages.success(
                request, 'Your message has been sent successfully!')
            # Redirect to the success page
            return redirect('contact:success')
    else:
        # Instantiate an empty form for GET requests
        form = ContactForm()

    # Render the contact form page
    return render(request, 'contact/contact_form.html', {'form': form})


def success_view(request):
    """
    Displays the success page after the contact form is submitted.
    """
    return render(request, 'contact/success.html')
