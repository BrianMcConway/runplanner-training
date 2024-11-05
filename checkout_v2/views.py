from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from .forms import OrderForm
from .models import Order, OrderLineItem
from products_v2.models import Product
from basket_v2.contexts import basket_contents

import stripe
import json

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def cache_checkout_data(request):
    """
    Caches checkout data for a payment intent using Stripe.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.get_username() if request.user.is_authenticated else 'Guest'
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

def checkout(request):
    """
    Handles the checkout process, including form validation and payment intent creation.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            client_secret = request.POST.get('client_secret', None)
            if client_secret:
                pid = client_secret.split('_secret')[0]
                order.stripe_pid = pid
                order.original_basket = json.dumps(basket)
                order.save()
                
                for item_id, item_data in basket.items():
                    try:
                        product = Product.objects.get(id=item_id)
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    except Product.DoesNotExist:
                        messages.error(request, "One of the products in your basket wasn't found in our database. Please call us for assistance!")
                        order.delete()
                        return redirect(reverse('basket_v2:show_basket'))

                request.session['save_info'] = 'save-info' in request.POST
                request.session['basket'] = {}  # Clear the basket after order creation
                return redirect(reverse('checkout_v2:checkout_success', args=[order.order_number]))
            else:
                messages.error(request, 'Client secret missing. Payment setup error, please try again.')
                return redirect(reverse('basket_v2:show_basket'))
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "You don't have anything in your basket!")
            return redirect(reverse('products_v2:training_plans'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Check your environment variables.')

    template = 'checkout_v2/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Renders the checkout success page, clears the basket, and confirms order processing.
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! A confirmation email will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout_v2/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
