from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import Order, OrderLineItem
from products_v2.models import Product
import json
import logging
import uuid
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """
    Sets up the Stripe Checkout session and redirects to the payment page.
    """
    if request.method == 'POST':
        # Retrieve basket from session
        basket = request.session.get('basket', {})
        line_items = []

        # Construct line items for Stripe from the basket
        for item_slug, item_data in basket.items():
            product = Product.objects.get(slug=item_slug)
            line_items.append({
                'price_data': {
                    'currency': 'usd',  # Update as needed
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),  # Amount in cents
                },
                'quantity': item_data['quantity'],
            })

        # Create the Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout_v2:order_success')),
            cancel_url=request.build_absolute_uri(reverse('checkout_v2:checkout')),
        )

        return redirect(session.url, code=303)

    return render(request, 'checkout_v2/checkout.html')

def create_order(request):
    """
    Creates an order in the backend and calculates prices based on the basket.
    """
    if request.method == 'POST':
        # Extract order data from POST request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        # Extract the full country from the form submission
        country = request.POST.get('country') if request.POST.get('country') else ''
        
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
            grand_total=order_total,  # Initialize with order total
            stripe_pid=stripe_pid,
            is_paid=False  # Set to unpaid initially
        )
        order.save()

        # Calculate total by iterating through parsed basket
        for item_slug, item_data in parsed_basket.items():
            logger.info("Attempting to retrieve product with slug: %s", item_slug)
            try:
                # Retrieve product based on slug
                product = Product.objects.get(slug=item_slug)
                
                # Extract the quantity from item_data dictionary
                quantity = item_data.get('quantity', 1)
                
                # Calculate line item total and add to order total
                line_item_total = product.price * quantity
                order_total += line_item_total

                # Create and save each line item with the correct product
                line_item = OrderLineItem(order=order, product=product, quantity=quantity, lineitem_total=line_item_total)
                line_item.save()

            except Product.DoesNotExist:
                logger.error("Product with slug %s not found in the database.", item_slug)
                continue

        # Update the order totals and save again
        order.order_total = order_total
        order.grand_total = order_total  # Adjust if other fees apply
        order.save()

        logger.info("Order created with ID: %s and Stripe PID: %s. Order total: %s", order.id, stripe_pid, order_total)

        # Redirect to a success page or order confirmation
        return redirect(reverse('checkout_v2:order_success_detail', args=[order.id]))

    # GET request: Render the order form, passing the basket to the template
    basket = request.session.get('basket', '{}')
    return render(request, 'checkout_v2/create_order.html', {'basket': json.dumps(basket)})

@csrf_exempt
def stripe_webhook(request):
    """
    Webhook endpoint for Stripe to handle events like checkout.session.completed.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        # Invalid payload or signature
        logger.error("Webhook signature verification failed: %s", e)
        return HttpResponse(status=400)

    # Process the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info("Processing checkout.session.completed event")
        handle_checkout_session(request, session)

    return HttpResponse(status=200)

def handle_checkout_session(request, session):
    """
    Handles the successful checkout session and updates the order.
    """
    stripe_pid = session.get('id')
    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
        order.is_paid = True
        order.save()

        # Store order ID and total in session for displaying on the success page
        request.session['order_id'] = order.id
        request.session['order_total'] = order.grand_total

        logger.info("Order %s marked as paid.", order.id)
    except Order.DoesNotExist:
        logger.error("Order with Stripe PID %s not found.", stripe_pid)

def order_success(request):
    """
    Displays a generic success message after an order has been completed.
    """
    order_id = request.session.get('order_id')
    order_total = request.session.get('order_total')

    # Clear the order data from session after using it
    request.session.pop('order_id', None)
    request.session.pop('order_total', None)

    return render(request, 'checkout_v2/order_success.html', {
        'order_id': order_id,
        'order_total': order_total
    })

def order_success_detail(request, order_id):
    """
    Displays a detailed success message for a specific order.
    """
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout_v2/order_success_detail.html', {'order': order})
