# checkout_v2/webhook_handler.py

import json
import stripe
from django.http import HttpResponse
from .models import Order
import logging

# Set up logger
logger = logging.getLogger(__name__)

class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle generic/unknown/unexpected webhook event"""
        logger.info(f"Unhandled event received: {event['type']}")
        return HttpResponse(
            content=f'Unhandled event received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket if 'basket' in intent.metadata else None
        save_info = intent.metadata.save_info if 'save_info' in intent.metadata else None

        # Log the event
        logger.info(f"PaymentIntent succeeded for PID: {pid}")

        # Fetch the order using the payment intent ID
        try:
            order = Order.objects.get(stripe_pid=pid)
            if order:
                order.is_paid = True  # Ensure `is_paid` field exists in Order model
                order.save()
                logger.info(f"Order {order.id} marked as paid")
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order in database',
                    status=200
                )
        except Order.DoesNotExist:
            logger.error(f"Order with PID {pid} not found in database")
            return HttpResponse(
                content=f'Order with PID {pid} not found',
                status=404
            )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        logger.warning(f"Payment failed for PID: {event.data.object.id}")
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Payment failed',
            status=200
        )
