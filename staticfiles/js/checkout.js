document.addEventListener("DOMContentLoaded", function () {
    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe public key or client secret is missing.");
        document.getElementById("card-errors").textContent = "Payment setup error. Please try again later.";
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const card = elements.create('card', { hidePostalCode: true });
    card.mount("#card-element");

    const form = document.getElementById("payment-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();

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
                console.error("Payment error:", result.error.message);
                document.getElementById("card-errors").textContent = result.error.message;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                } else {
                    console.error("Unexpected payment status:", result.paymentIntent.status);
                }
            }
        }).catch(error => {
            console.error("JS error during payment submission:", error);
        });
    });
});
