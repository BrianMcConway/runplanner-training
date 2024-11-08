import json
import stripe
from django.http import HttpResponse
from .models import Order, OrderLineItem
from products_v2.models import Product
import logging

logger = logging.getLogger(__name__)

class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic/unexpected webhook event"""
        logger.info(f"Unhandled event received: {event['type']}")
        return HttpResponse(
            content=f'Unhandled event received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event['data']['object']
        pid = intent.id
        metadata = intent.metadata

        # Order details from metadata
        basket = json.loads(metadata.get('basket', '{}'))
        full_name = metadata.get('full_name')
        email = intent.charges.data[0].billing_details.email
        phone_number = metadata.get('phone_number')
        country = metadata.get('country', '')
        town_or_city = metadata.get('town_or_city', '')
        street_address1 = metadata.get('street_address1', '')
        street_address2 = metadata.get('street_address2', '')
        county = metadata.get('county', '')
        postcode = metadata.get('postcode', '')

        # Try retrieving or creating the order
        try:
            order = Order.objects.get(stripe_pid=pid)
            logger.info(f"Order {order.id} already exists.")
        except Order.DoesNotExist:
            order_total = 0
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
                original_basket=json.dumps(basket),
                order_total=0,
                grand_total=0,
                stripe_pid=pid,
                is_paid=True
            )
            order.save()

            # Add line items
            for item_slug, item_data in basket.items():
                try:
                    product = Product.objects.get(slug=item_slug)
                    quantity = item_data.get('quantity', 1)
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

            # Update totals
            order.order_total = order_total
            order.grand_total = order_total
            order.save()
            logger.info(f"Order {order.id} created successfully.")

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Order processed successfully',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        logger.warning(f"Payment failed for PID: {event['data']['object'].id}")
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Payment failed',
            status=200
        )
