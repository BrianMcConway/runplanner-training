// checkout.js

document.addEventListener("DOMContentLoaded", function () {
    const stripePublicKey = document.getElementById("id_stripe_public_key").textContent.trim();
    const clientSecret = document.getElementById("id_client_secret").textContent.trim();

    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe public key or client secret is missing.");
        document.getElementById("card-errors").textContent = "Payment setup error. Please try again later.";
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const cardStyle = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };
    const card = elements.create('card', { style: cardStyle, hidePostalCode: true });
    card.mount("#card-element");

    card.on('change', function (event) {
        const errorDiv = document.getElementById('card-errors');
        errorDiv.textContent = event.error ? event.error.message : '';
    });

    let formSubmitting = false;
    const form = document.getElementById("payment-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        if (formSubmitting) return;

        formSubmitting = true;
        document.getElementById("submit-button").disabled = true;

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
                console.error("Payment error:", result.error.message);  // Log the error for easier troubleshooting
                document.getElementById("card-errors").textContent = result.error.message;
                document.getElementById("submit-button").disabled = false;
                formSubmitting = false;
            } else {
                if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                    console.log("Payment succeeded:", result.paymentIntent);
                    form.submit();
                } else {
                    console.warn("Unexpected payment intent status:", result.paymentIntent);
                    document.getElementById("card-errors").textContent = "Payment could not be completed. Please try again.";
                    document.getElementById("submit-button").disabled = false;
                    formSubmitting = false;
                }
            }
        }).catch(function (error) {
            console.error("Unhandled promise rejection:", error);
            document.getElementById("card-errors").textContent = "An error occurred. Please try again later.";
            document.getElementById("submit-button").disabled = false;
            formSubmitting = false;
        });
    });
});
