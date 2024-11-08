import json
import time
from django.http import HttpResponse
from .models import Order, OrderLineItem
from products_v2.models import Product
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event['data']['object']
        pid = intent.id
        metadata = intent.metadata

        # Extract order details from metadata
        basket = metadata.get('basket', '{}')
        full_name = metadata.get('full_name', '')
        email = metadata.get('email', '')
        phone_number = metadata.get('phone_number', '')
        country = metadata.get('country', '')
        town_or_city = metadata.get('town_or_city', '')
        street_address1 = metadata.get('street_address1', '')
        street_address2 = metadata.get('street_address2', '')
        county = metadata.get('county', '')
        postcode = metadata.get('postcode', '')

        # Attempt to find the order in the database
        order_exists = False
        attempt = 1
        order = None
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=full_name,
                    email__iexact=email,
                    phone_number__iexact=phone_number,
                    country__iexact=country,
                    postcode__iexact=postcode,
                    town_or_city__iexact=town_or_city,
                    street_address1__iexact=street_address1,
                    street_address2__iexact=street_address2,
                    county__iexact=county,
                    grand_total=round(intent.amount_received / 100, 2),
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            # Order already exists
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        else:
            # Create the order since it does not exist
            try:
                order_total = 0
                order = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    country=country,
                    town_or_city=town_or_city,
                    street_address1=street_address1,
                    street_address2=street_address2,
                    county=county,
                    postcode=postcode,
                    original_basket=basket,
                    stripe_pid=pid,
                    is_paid=True
                )

                # Deserialize the basket JSON string
                parsed_basket = json.loads(basket)

                # Create OrderLineItems from basket data
                for item_slug, item_data in parsed_basket.items():
                    try:
                        product = Product.objects.get(slug=item_slug)
                        quantity = int(item_data.get('quantity', 1))
                        line_item_total = product.price * quantity
                        order_total += line_item_total

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

                # Update the order with calculated totals and save again
                order.order_total = order_total
                order.grand_total = order_total
                order.save()

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                    status=200
                )
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                    status=500
                )

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed webhook from Stripe
        """
        session = event['data']['object']
        # Retrieve the PaymentIntent ID from the session object
        payment_intent_id = session.get('payment_intent')
        # Use the PaymentIntent ID to retrieve the payment intent object
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        # Process the payment intent as in handle_payment_intent_succeeded
        return self.handle_payment_intent_succeeded({'data': {'object': payment_intent}})

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_checkout_session_expired(self, event):
        """
        Handle the checkout.session.expired webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Handled checkout.session.expired',
            status=200
        )
