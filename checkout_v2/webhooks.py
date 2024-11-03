from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
import logging
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def stripe_webhook(request):
    """Listen for Stripe webhooks and handle payment intent events."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid payload.")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Webhook signature verification failed.")
        return HttpResponse(status=400)

    # Event handling
    if event['type'] == 'payment_intent.succeeded':
        handle_payment_intent_succeeded(event)
    elif event['type'] == 'payment_intent.payment_failed':
        handle_payment_intent_failed(event)
    else:
        logger.info(f"Unhandled event type: {event['type']}")

    return HttpResponse(status=200)

def handle_payment_intent_succeeded(event):
    """Handle the payment_intent.succeeded event."""
    payment_intent = event['data']['object']
    stripe_pid = payment_intent['id']
    amount_received = payment_intent['amount_received']
    currency = payment_intent['currency']

    logger.info(f"Payment intent succeeded for PID: {stripe_pid}, amount: {amount_received / 100} {currency.upper()}")

    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
        if not order.is_paid:
            order.is_paid = True
            order.save()
            logger.info(f"Order {order.id} marked as paid.")
    except Order.DoesNotExist:
        logger.warning(f"No order found for PID: {stripe_pid}")

def handle_payment_intent_failed(event):
    """Handle the payment_intent.payment_failed event."""
    payment_intent = event['data']['object']
    stripe_pid = payment_intent['id']
    logger.error(f"Payment intent failed for PID: {stripe_pid}")
