from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Order, OrderLineItem
from products_v2.models import Product
import json
import uuid
import stripe
from my_account.models import Purchase
from basket_v2.models import BasketItem  # Import BasketItem

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='account_login')
def checkout(request):
    """
    Render the checkout page with the Stripe public key and basket data.
    """
    # Save intended checkout path in session for post-login redirection
    if not request.user.is_authenticated:
        request.session['next'] = 'checkout_v2:checkout'
        return redirect('account_login')
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    # Check if user has persistent basket items
    items = []
    total_price = 0

    if request.user.is_authenticated:
        # Use persistent basket items for logged-in users
        basket_items = BasketItem.objects.filter(user=request.user)
        if not basket_items.exists():
            return redirect('basket_v2:show_basket')  # Redirect if basket is empty

        for basket_item in basket_items:
            line_item_total = basket_item.product.price * basket_item.quantity
            total_price += line_item_total
            items.append({
                'name': basket_item.product.name,
                'price': f'€{basket_item.product.price:.2f}',
                'quantity': basket_item.quantity
            })
    else:
        # Use session-based basket for non-logged-in users
        original_basket = request.session.get('basket', '{}')
        try:
            parsed_basket = json.loads(original_basket) if isinstance(original_basket, str) else original_basket
        except json.JSONDecodeError:
            parsed_basket = {}

        for item_slug, item_data in parsed_basket.items():
            try:
                product = Product.objects.get(slug=item_slug)
                quantity = int(item_data.get('quantity', 1))
                line_item_total = product.price * quantity
                total_price += line_item_total
                items.append({'name': product.name, 'price': f'€{product.price:.2f}', 'quantity': quantity})
            except Product.DoesNotExist:
                continue

    context = {
        'stripe_public_key': stripe_public_key,
        'items': items,
        'total_price': f'€{total_price:.2f}'
    }
    return render(request, 'checkout_v2/checkout.html', context)

@login_required(login_url='account_login')
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

        # Check if the user has a persistent basket or session basket
        items = []
        total_price = 0

        if request.user.is_authenticated:
            # Use persistent basket items
            basket_items = BasketItem.objects.filter(user=request.user)
            if not basket_items.exists():
                return JsonResponse({'error': 'Your basket is empty.'})

            for basket_item in basket_items:
                product = basket_item.product
                quantity = basket_item.quantity
                line_item_total = product.price * quantity
                total_price += line_item_total
                items.append((product, quantity))
        else:
            # Fallback to session-based basket for non-logged-in users
            original_basket = request.session.get('basket', '{}')
            try:
                parsed_basket = json.loads(original_basket) if isinstance(original_basket, str) else original_basket
            except json.JSONDecodeError:
                parsed_basket = {}

            if not parsed_basket:
                return JsonResponse({'error': 'Your basket is empty.'})

            for item_slug, item_data in parsed_basket.items():
                try:
                    product = Product.objects.get(slug=item_slug)
                    quantity = int(item_data.get('quantity', 1))
                    line_item_total = product.price * quantity
                    total_price += line_item_total
                    items.append((product, quantity))
                except Product.DoesNotExist:
                    continue

        # Generate a unique stripe_pid and initialize totals
        stripe_pid = str(uuid.uuid4())
        order_total = total_price

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
            original_basket=json.dumps(parsed_basket if not request.user.is_authenticated else {}),
            order_total=order_total,
            grand_total=order_total,
            stripe_pid=stripe_pid,
            is_paid=False
        )
        order.save()

        # Calculate totals and create order line items
        for product, quantity in items:
            line_item_total = product.price * quantity
            line_item = OrderLineItem(
                order=order,
                product=product,
                quantity=quantity,
                lineitem_total=line_item_total
            )
            line_item.save()

        # Update the order with the calculated totals
        order.order_total = order_total
        order.grand_total = order_total
        order.save()

        # Serialize basket for metadata
        basket_json = json.dumps(parsed_basket if not request.user.is_authenticated else {})

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
        order.stripe_pid = stripe_pid
        order.save()

        # Return client_secret and order_id to the client
        return JsonResponse({
            'client_secret': intent.client_secret,
            'order_id': order.id
        })

    # If not POST request, return an error
    return JsonResponse({'error': 'Invalid request method.'})

@login_required(login_url='account_login')
def check_order_payment(request, order_id):
    """
    Returns the payment status of the order as JSON.
    """
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'is_paid': order.is_paid})

@login_required(login_url='account_login')
def order_success(request, order_id):
    """
    Display a success message after an order has been completed.
    Show the order details for confirmation and clear the basket.
    """
    # Retrieve the order object by ID
    order = get_object_or_404(Order, id=order_id)

    # Create purchase records for each line item in the order
    for line_item in order.lineitems.all():
        Purchase.objects.create(
            user=request.user,
            training_plan=line_item.product,
            purchase_date=timezone.now(),
            payment_verified=True
        )

    # Clear the persistent basket for authenticated users
    if request.user.is_authenticated:
        BasketItem.objects.filter(user=request.user).delete()
    # Clear the session basket as a fallback
    if 'basket' in request.session:
        del request.session['basket']

    # Render the checkout success page with the order details
    return render(request, 'checkout_v2/checkout_success.html', {'order': order})
