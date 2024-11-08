from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from .models import Order, OrderLineItem
from products_v2.models import Product
import json
import uuid
import stripe

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """
    Handle the checkout process, including creating the order,
    calculating totals, and creating the Stripe Payment Intent.
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

        # Parse the basket data into a dictionary
        try:
            parsed_basket = json.loads(original_basket) if isinstance(original_basket, str) else original_basket
        except json.JSONDecodeError:
            parsed_basket = {}

        # Generate a unique Stripe PID and initialize totals
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

        # Pass data to the template for frontend processing
        context = {
            'order': order,
            'order_id': order.id,  # For JavaScript use
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret
        }

        return render(request, 'checkout_v2/checkout.html', context)

    # For GET requests, render the checkout form
    basket = request.session.get('basket', '{}')
    return render(request, 'checkout_v2/checkout.html', {'basket': json.dumps(basket)})

def order_success(request, order_id):
    """
    Display a success message after an order has been completed.
    Show the order details for confirmation and clear the basket.
    """
    order = Order.objects.get(id=order_id)

    # Clear the session basket
    if 'basket' in request.session:
        del request.session['basket']

    return render(request, 'checkout_v2/checkout_success.html', {'order': order})
