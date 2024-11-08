import json
import time
from django.http import HttpResponse
from .models import Order, OrderLineItem
from products_v2.models import Product
import logging

logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        logger.info(f'Unhandled webhook received: {event["type"]}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
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

        # Try to retrieve the order, with retries
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
                logger.info(f"Order {order.id} already exists in the database.")
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        else:
            # Order does not exist, create it
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
                        logger.error(f"Product with slug {item_slug} not found.")
                        continue

                # Update the order with calculated totals and save again
                order.order_total = order_total
                order.grand_total = order_total
                order.save()
                logger.info(f"Order {order.id} created with total: {order.grand_total}")

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                    status=200
                )
            except Exception as e:
                if order:
                    order.delete()
                logger.error(f"Error creating order: {e}")
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        logger.warning(f"Payment failed for PID: {event['data']['object'].id}")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
