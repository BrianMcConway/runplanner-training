from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
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
            order.original_basket = json.dumps(basket)
            order.save()

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

            # Prepare Stripe payment intent
            stripe_total = round(order.grand_total * 100)
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                metadata={
                    'order_id': order.id,
                    'basket': json.dumps(basket)  # Optional: for reference only
                }
            )

            # Save Stripe payment intent ID for later verification
            order.stripe_pid = intent.id
            order.save()

            # Temporarily save order ID in the session for confirmation
            request.session['order_id'] = order.id

            return render(request, 'checkout_v2/checkout.html', {
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                'total': order.grand_total,
            })

        else:
            messages.error(request, "Check your information.")
            return redirect('basket_v2:show_basket')

    # Handle GET requests to retrieve basket contents and create a PaymentIntent
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty!")
            return redirect('products_v2:training_plans')

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)

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

def checkout_success(request):
    """Displays success message and clears basket upon confirmed payment."""
    order_id = request.session.pop('order_id', None)
    if not order_id:
        messages.error(request, "No order found.")
        return redirect('products_v2:training_plans')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('products_v2:training_plans')

    # Clear the basket from session after successful order
    request.session.pop('basket', None)

    messages.success(request, f"Thank you for your order! Your order number is {order.id}.")
    return redirect('checkout_v2:order_complete', order_id=order.id)

@require_POST
def stripe_webhook(request):
    """Listen for Stripe webhooks to confirm payment status and complete the order."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle successful payment intent
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        stripe_pid = payment_intent['id']
        order = Order.objects.filter(stripe_pid=stripe_pid).first()
        if order:
            # Mark the order as paid or update any status as necessary
            order.save()

    return HttpResponse(status=200)
