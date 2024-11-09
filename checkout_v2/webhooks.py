from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
@csrf_exempt
def stripe_webhook(request):
    """
    Listen for webhooks from Stripe and handle incoming events.
    """
    # Retrieve the webhook data and verify its signature
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        # Construct the event using Stripe's library
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # Other exceptions
        return HttpResponse(content=str(e), status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to their handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
        'checkout.session.completed': handler.handle_checkout_session_completed,
        'checkout.session.expired': handler.handle_checkout_session_expired,
    }

    # Get the event type
    event_type = event['type']

    # Get the appropriate handler function
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the handler function with the event
    response = event_handler(event)
    return response
