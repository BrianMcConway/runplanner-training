from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderLineItem
from products_v2.models import Product
import json
import logging
import uuid

logger = logging.getLogger(__name__)

def checkout(request):
    """
    Main checkout view placeholder.
    Renders the checkout form where Stripe or other payment integrations can be added.
    """
    return render(request, 'checkout_v2/checkout.html')

def create_order(request):
    """
    View to create an order in the backend, without requiring Stripe confirmation.
    Handles order data submission via POST and calculates prices based on the basket.
    """
    if request.method == 'POST':
        # Extract order data from POST request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        # Ensure only the first two characters are taken for the country code
        country = request.POST.get('country')[:2] if request.POST.get('country') else ''
        
        town_or_city = request.POST.get('town_or_city')
        street_address1 = request.POST.get('street_address1')
        street_address2 = request.POST.get('street_address2')
        county = request.POST.get('county')
        postcode = request.POST.get('postcode', '')

        # Get the basket data from the POST request
        original_basket = request.POST.get('basket', '{}')
        
        # Log the basket data before parsing
        logger.info("Original basket data: %s", original_basket)

        # Parse the basket data into a dictionary
        try:
            parsed_basket = json.loads(original_basket)  # Parse basket into dict
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
            country=country,  # Store country code only to fit field constraints
            town_or_city=town_or_city,
            street_address1=street_address1,
            street_address2=street_address2,
            county=county,
            postcode=postcode,
            date=timezone.now(),
            original_basket=original_basket,
            order_total=order_total,
            grand_total=order_total,  # Initialize with order total
            stripe_pid=stripe_pid,  # Unique for each order
            is_paid=False  # Set to unpaid initially
        )
        order.save()

        # Calculate total by iterating through parsed basket
        for item_id, quantity in parsed_basket.items():
            logger.info("Attempting to retrieve product with ID: %s", item_id)
            try:
                # Retrieve the correct product based on item_id
                product = Product.objects.get(id=item_id)
                line_item_total = product.price * quantity
                order_total += line_item_total

                # Create and save each line item with the correct product
                line_item = OrderLineItem(order=order, product=product, quantity=quantity, lineitem_total=line_item_total)
                line_item.save()

            except Product.DoesNotExist:
                logger.error("Product with ID %s not found in the database.", item_id)
                continue

        # Update the order totals and save again
        order.order_total = order_total
        order.grand_total = order_total  # Adjust if other fees apply
        order.save()

        logger.info("Order created with ID: %s and Stripe PID: %s. Order total: %s", order.id, stripe_pid, order_total)

        # Redirect to a success page or order confirmation
        return redirect(reverse('checkout_v2:order_success', args=[order.id]))

    # GET request: Render the order form (use for testing)
    return render(request, 'checkout_v2/create_order.html')

def order_success(request, order_id):
    """
    Displays a success message after an order has been created.
    Shows the order details for confirmation.
    """
    order = Order.objects.get(id=order_id)
    return render(request, 'checkout_v2/order_success.html', {'order': order})
