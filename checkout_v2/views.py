from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products_v2.models import Product
from basket_v2.contexts import basket_contents
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """Handles the checkout process, payment intent creation, and displays a success message."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty!")
            return redirect('products_v2:training_plans')

        form_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'country': request.POST.get('country'),
            'postcode': request.POST.get('postcode'),
            'town_or_city': request.POST.get('town_or_city'),
            'street_address1': request.POST.get('street_address1'),
            'street_address2': request.POST.get('street_address2'),
            'county': request.POST.get('county'),
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Save the order temporarily
            order = order_form.save(commit=False)
            order.original_basket = json.dumps(basket)
            order.save()

            # Add line items to the order
            for item_id, item_data in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, "One of the products in your basket wasn't found.")
                    order.delete()  # Remove the incomplete order
                    return redirect('basket_v2:show_basket')

            # Prepare Stripe payment intent
            stripe_total = round(order.grand_total * 100)  # Ensure total is correctly calculated
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    'order_id': order.id,
                    'basket': json.dumps(basket)  # Optional metadata
                }
            )

            # Save Stripe payment intent ID for order verification
            order.stripe_pid = intent.id
            order.save()

            # Temporarily save order ID in session for success page handling
            request.session['order_id'] = order.id

            return render(request, 'checkout_v2/checkout.html', {
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                'total': order.grand_total,
            })

        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
            return redirect('basket_v2:show_basket')

    else:  # Handle GET request
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty!")
            return redirect('products_v2:training_plans')

        # Calculate the current basket total
        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)  # Stripe expects amount in cents

        # Create a new payment intent for the checkout page
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()  # Blank form for GET request

        return render(request, 'checkout_v2/checkout.html', {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'total': total,
        })

def checkout_success(request):
    """Displays success message and clears basket upon confirmed payment."""
    order_id = request.session.pop('order_id', None)
    if not order_id:
        messages.error(request, "No order found.")
        return redirect('products_v2:training_plans')

    try:
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('products_v2:training_plans')

    # Clear the basket from session after successful order
    request.session.pop('basket', None)

    messages.success(request, f"Thank you for your order! Your order number is {order.id}.")
    
    # Redirect to an order complete or summary page
    return redirect('checkout_v2:order_complete', order_id=order.id)
