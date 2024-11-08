from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
from .models import Order, OrderLineItem
from products_v2.models import Product
from .webhook_handler import StripeWH_Handler
import json
import logging
import uuid
import stripe

logger = logging.getLogger(__name__)

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def checkout(request):
    """
    Main checkout view that handles Stripe payment processing and order creation.
    """
    if request.method == 'POST':
        # Extract order data from POST request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')[:2] if request.POST.get('country') else ''
        town_or_city = request.POST.get('town_or_city')
        street_address1 = request.POST.get('street_address1')
        street_address2 = request.POST.get('street_address2')
        county = request.POST.get('county')
        postcode = request.POST.get('postcode', '')

        # Retrieve basket from session, or use empty if not set
        original_basket = request.session.get('basket', '{}')
        
        # Log the basket data before parsing
        logger.info("Original basket data from session: %s", original_basket)

        # Parse the basket data into a dictionary
        try:
            parsed_basket = json.loads(original_basket) if isinstance(original_basket, str) else original_basket
            logger.info("Parsed basket data: %s", parsed_basket)
        except json.JSONDecodeError as e:
            logger.error("Error parsing basket data: %s", e)
            parsed_basket = {}

        # Set up unique Stripe PID and initialize totals
        stripe_pid = str(uuid.uuid4())  # Generate unique stripe_pid
        order_total = 0

        # Create an Order instance
        order = Order(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            country=country,
            town_or_city=town_or_city,
            street_address1=street_address1,
            street_address2=street_address2,
            county=county,
            postcode=postcode,
            date=timezone.now(),
            original_basket=json.dumps(parsed_basket),
            order_total=order_total,
            grand_total=order_total,
            stripe_pid=stripe_pid,
            is_paid=False
        )
        order.save()

        # Calculate total by iterating through parsed basket, retrieving products by slug
        for item_slug, item_data in parsed_basket.items():
            logger.info("Attempting to retrieve product with slug: %s", item_slug)
            try:
                # Retrieve product based on slug
                product = Product.objects.get(slug=item_slug)
                
                # Extract the quantity from item_data dictionary
                quantity = int(item_data.get('quantity', 1))  # Ensure quantity is an integer
                
                # Calculate line item total and add to order total
                line_item_total = product.price * quantity
                order_total += line_item_total

                # Create and save each line item with the correct product
                line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    lineitem_total=line_item_total
                )
                line_item.save()

            except Product.DoesNotExist:
                logger.error("Product with slug %s not found in the database.", item_slug)
                continue

        # Update the order totals and save again
        order.order_total = order_total
        order.grand_total = order_total
        order.save()

        # Serialize basket for metadata
        basket_json = json.dumps(parsed_basket)

        # Ensure metadata values are strings and within Stripe's limitations
        metadata = {
            'order_id': str(order.id),
            'stripe_pid': stripe_pid,
            'basket': basket_json,
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'country': country,
            'town_or_city': town_or_city,
            'street_address1': street_address1,
            'street_address2': street_address2,
            'county': county,
            'postcode': postcode,
        }

        # Truncate metadata values if necessary to comply with Stripe's limits
        for key, value in metadata.items():
            if isinstance(value, str) and len(value) > 500:
                metadata[key] = value[:500]

        # Create Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=int(order.grand_total * 100),  # Stripe expects amount in cents
            currency='eur',
            metadata=metadata
        )

        # Pass order and Stripe client secret to the template for the frontend confirmation
        context = {
            'order': order,
            'order_id': order.id,  # Explicitly passing order_id for JavaScript
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret
        }

        return render(request, 'checkout_v2/checkout.html', context)

    # GET request: Render the checkout form with an empty basket if not provided
    basket = request.session.get('basket', '{}')
    return render(request, 'checkout_v2/checkout.html', {'basket': json.dumps(basket)})

def order_success(request, order_id):
    """
    Displays a success message after an order has been created.
    Shows the order details for confirmation and clears the basket.
    """
    order = Order.objects.get(id=order_id)

    # Clear the session basket
    if 'basket' in request.session:
        del request.session['basket']

    return render(request, 'checkout_v2/checkout_success.html', {'order': order})

def stripe_webhook(request):
    """Listen for webhooks from Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Signature verification failed: {e}")
        return HttpResponse(status=400)

    # Set up a Stripe webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the event type
    event_type = event['type']

    # Use the event handler from the map or fallback to the default handler
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
