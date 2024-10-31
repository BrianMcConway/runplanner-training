from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .forms import OrderForm
from .models import Order, OrderLineItem
from products_v2.models import Product
from basket_v2.contexts import basket_contents
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """Handles the checkout process, payment, and success display."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty!")
            return redirect('products_v2:training_plans')

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            print(f"Order created: ID - {order.id}, Total - {order.grand_total}")  # Debug

            # Add line items
            for item_id, item_data in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(order=order, product=product, quantity=item_data)
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, "One of the products in your basket wasn't found.")
                    order.delete()
                    return redirect('basket_v2:show_basket')

            # Create Stripe payment intent
            stripe_total = round(order.grand_total * 100)
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
            print(f"Payment Intent: {intent.id}")  # Debug Stripe Payment Intent creation
            # Return checkout page with confirmation variables
            return render(request, 'checkout_v2/checkout.html', {
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                'total': order.grand_total,
                'order_id': order.id,
                'success_message': "Order processed successfully!"  # Success message directly here
            })

        messages.error(request, "Check your information.")
        return redirect('basket_v2:show_basket')
    
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "You don't have anything in your basket!")
            return redirect('products_v2:training_plans')

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)

        # Payment Intent for card payment
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        order_form = OrderForm()
        return render(request, 'checkout_v2/checkout.html', {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'total': total,
        })
