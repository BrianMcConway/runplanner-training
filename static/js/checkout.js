document.addEventListener("DOMContentLoaded", function () {
    // Retrieve public key and client secret
    const stripePublicKey = document.getElementById("id_stripe_public_key").textContent;
    const clientSecret = document.getElementById("id_client_secret").textContent;

    // Check if keys are available
    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe public key or client secret is missing.");
        document.getElementById("card-errors").textContent = "Payment setup error. Please try again later.";
        return;
    }

    // Initialize Stripe and Elements
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const card = elements.create('card', { hidePostalCode: true });
    card.mount("#card-element");

    // Handle form submission
    const form = document.getElementById("payment-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        document.getElementById("submit-button").disabled = true;

        // Confirm payment with Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.full_name.value,
                    email: form.email.value,
                    phone: form.phone_number.value,
                    address: {
                        line1: form.street_address1.value,
                        line2: form.street_address2.value,
                        city: form.town_or_city.value,
                        country: form.country.value,
                        state: form.county.value,
                    }
                }
            }
        }).then(function (result) {
            if (result.error) {
                console.log("Payment error:", result.error.message);
                document.getElementById("card-errors").textContent = result.error.message;
                document.getElementById("submit-button").disabled = false;
            } else if (result.paymentIntent.status === 'succeeded') {
                console.log("Payment succeeded, redirecting to success page.");

                // Redirect to the order success page
                const orderSuccessUrl = form.action.replace('checkout', 'order_success/' + result.paymentIntent.metadata.order_id);
                window.location.href = orderSuccessUrl;
            }
        });
    });
});
