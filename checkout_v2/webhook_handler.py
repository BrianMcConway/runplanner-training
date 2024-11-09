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
        order_id = metadata.get('order_id')
        try:
            order = Order.objects.get(id=order_id, stripe_pid=pid)
            order.is_paid = True
            order.save()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        except Order.DoesNotExist:
            # Order does not exist, handle accordingly
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order not found.',
                status=500
            )

    def handle_checkout_session_completed(self, event):
        """
        Handle the checkout.session.completed webhook from Stripe
        """
        return self.handle_payment_intent_succeeded(event)

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
