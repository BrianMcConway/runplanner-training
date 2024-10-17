from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CheckoutForm
from .models import OrderItem, Order
from basket.basket import Basket
import stripe
from django.contrib import messages

# Set Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Helper function to create a payment intent with Stripe
def create_payment_intent(order):
    stripe_total = int(order.total_amount * 100)  # Stripe requires amounts in cents
    return stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=order.currency,
        metadata={'order_id': order.id}
    )

# View to handle both checkout form submission and payment
def checkout_view(request):
    basket = Basket(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save order details
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.total_amount = basket.get_total_price()

            # Ensure total amount is valid
            if order.total_amount < 0.50:  # Stripe minimum amount validation
                messages.error(request, "The total amount must be at least €0.50 to complete the payment.")
                return redirect('checkout:checkout_view')

            order.save()

            # Save each item in the basket as OrderItem
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    training_plan=None,  # Since we're using dynamic plans, there's no actual ForeignKey
                    quantity=item['quantity'],
                    price=item['price'],
                    # Remove 'details' to avoid TypeError
                )

            # Create a payment intent with Stripe
            intent = create_payment_intent(order)

            # Pass form data and payment info back to the template
            return render(request, 'checkout/checkout.html', {
                'form': form,
                'basket': basket,
                'client_secret': intent.client_secret,  # For Stripe Payment
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            })
    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'basket': basket,
    })

# Payment success view
def payment_success(request):
    basket = Basket(request)
    basket.clear()  # Clear the basket after successful payment
    return render(request, 'checkout/payment_success.html')

# Payment error view
def payment_error(request):
    return render(request, 'checkout/payment_error.html')
