from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Order, OrderLineItem
from products_v2.models import Product
import json
import uuid
import stripe
from my_account.models import Purchase

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """
    Render the checkout page with the Stripe public key.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    return render(request, 'checkout_v2/checkout.html', {'stripe_public_key': stripe_public_key})

def create_order(request):
    """
    Handle the creation of an order via AJAX and return client_secret and order_id.
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

        # Retrieve basket from session
        original_basket = request.session.get('basket', '{}')

        # Parse the basket data into a dictionary
        try:
            parsed_basket = json.loads(original_basket) if isinstance(original_basket, str) else original_basket
        except json.JSONDecodeError:
            parsed_basket = {}

        if not parsed_basket:
            return JsonResponse({'error': 'Your basket is empty.'})

        # Generate a unique stripe_pid and initialize totals
        stripe_pid = str(uuid.uuid4())
        order_total = 0

        # Create an Order instance with initial data
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

        # Calculate totals and create order line items
        for item_slug, item_data in parsed_basket.items():
            try:
                # Retrieve the product based on slug
                product = Product.objects.get(slug=item_slug)

                # Extract quantity and calculate totals
                quantity = int(item_data.get('quantity', 1))
                line_item_total = product.price * quantity
                order_total += line_item_total

                # Create and save the order line item
                line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    lineitem_total=line_item_total
                )
                line_item.save()

            except Product.DoesNotExist:
                # Skip items that are not found
                continue

        # Update the order with the calculated totals
        order.order_total = order_total
        order.grand_total = order_total
        order.save()

        # Serialize basket for metadata
        basket_json = json.dumps(parsed_basket)

        # Prepare metadata for Stripe Payment Intent
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

        # Truncate metadata values to comply with Stripe's limits
        for key, value in metadata.items():
            if isinstance(value, str) and len(value) > 500:
                metadata[key] = value[:500]

        # Create the Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=int(order.grand_total * 100),  # Amount in cents
            currency='eur',
            metadata=metadata
        )

        # Save the stripe_pid (PaymentIntent ID) to the order
        order.stripe_pid = stripe_pid  # We use the generated stripe_pid
        order.save()

        # Return client_secret and order_id to the client
        return JsonResponse({
            'client_secret': intent.client_secret,
            'order_id': order.id
        })

    # If not POST request, return an error
    return JsonResponse({'error': 'Invalid request method.'})

def check_order_payment(request, order_id):
    """
    Returns the payment status of the order as JSON.
    """
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'is_paid': order.is_paid})

def order_success(request, order_id):
    """
    Display a success message after an order has been completed.
    Show the order details for confirmation and clear the basket.
    """
    # Retrieve the order object by ID
    order = get_object_or_404(Order, id=order_id)
    
    # Create purchase records for each line item in the order
    # Use the related_name 'lineitems' to access related OrderLineItem instances
    for line_item in order.lineitems.all():
        Purchase.objects.create(
            user=request.user,
            training_plan=line_item.product,  # Assuming 'product' is the training plan
            purchase_date=timezone.now(),
            payment_verified=True  # Mark as verified since payment was successful
        )

    # Clear the session basket
    if 'basket' in request.session:
        del request.session['basket']

    # Render the checkout success page with the order details
    return render(request, 'checkout_v2/checkout_success.html', {'order': order})