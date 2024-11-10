import json
import logging
from django.http import HttpResponse
from .models import Order, OrderLineItem
from products_v2.models import Product
import stripe
from django.conf import settings
import time

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logging
logger = logging.getLogger(__name__)

class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        logger.info(f'Unhandled webhook received: {event["type"]}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200  # Respond with 200 to acknowledge receipt
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        logger.info('Received payment_intent.succeeded webhook event')
        intent = event['data']['object']
        pid = intent.id
        metadata = intent.metadata
        logger.debug(f'PaymentIntent ID: {pid}')
        logger.debug(f'Metadata: {metadata}')

        # Extract order details from metadata
        order_id = metadata.get('order_id')
        stripe_pid = metadata.get('stripe_pid')

        try:
            order = Order.objects.get(id=order_id, stripe_pid=stripe_pid)
            order.is_paid = True
            order.save()
            logger.info(f'Order {order_id} marked as paid.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order updated.',
                status=200
            )
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found.',
                status=500
            )

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed webhook from Stripe
        """
        logger.info('Received checkout.session.completed webhook event')
        session = event['data']['object']
        logger.debug(f'Checkout Session ID: {session.id}')

        # Optionally, you can extract more data from the session object if needed
        # For now, we'll call the payment_intent.succeeded handler
        return self.handle_payment_intent_succeeded(event)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        logger.warning(f'Payment failed for PaymentIntent {event["data"]["object"]["id"]}')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200  # Acknowledge receipt
        )

    def handle_checkout_session_expired(self, event):
        """
        Handle the checkout.session.expired webhook from Stripe
        """
        logger.info(f'Checkout session expired for Session ID {event["data"]["object"]["id"]}')
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Handled checkout.session.expired',
            status=200
        )

    def handle_charge_succeeded(self, event):
        """
        Handle the charge.succeeded webhook from Stripe
        """
        logger.info('Received charge.succeeded webhook event')
        charge = event['data']['object']
        logger.debug(f'Charge ID: {charge["id"]}')
        metadata = charge.get('metadata', {})
        logger.debug(f'Metadata: {metadata}')

        # Extract order details from metadata
        order_id = metadata.get('order_id')
        stripe_pid = metadata.get('stripe_pid')

        try:
            order = Order.objects.get(id=order_id, stripe_pid=stripe_pid)
            order.is_paid = True
            order.save()
            logger.info(f'Order {order_id} marked as paid via charge.succeeded.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order updated.',
                status=200
            )
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found.',
                status=500
            )

    def handle_charge_updated(self, event):
        """
        Handle the charge.updated webhook from Stripe
        """
        logger.info('Received charge.updated webhook event')
        charge = event['data']['object']
        logger.debug(f'Charge ID: {charge["id"]}')
        metadata = charge.get('metadata', {})
        logger.debug(f'Metadata: {metadata}')

        # Example: Update order details or log the update
        order_id = metadata.get('order_id')
        stripe_pid = metadata.get('stripe_pid')

        try:
            order = Order.objects.get(id=order_id, stripe_pid=stripe_pid)
            # Example: Update order details based on charge update
            # You can add more logic here as per your requirements
            logger.info(f'Order {order_id} charge updated.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Charge updated.',
                status=200
            )
        except Order.DoesNotExist:
            logger.error(f'Order {order_id} not found for charge update.')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found.',
                status=500
            )
