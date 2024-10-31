from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Order
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def stripe_webhook(request):
    """Listen for Stripe webhooks to confirm payment status and complete the order."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle successful payment intent
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        stripe_pid = payment_intent['id']
        order = Order.objects.filter(stripe_pid=stripe_pid).first()
        if order:
            # Mark the order as paid or update status as necessary
            order.save()

    return HttpResponse(status=200)
