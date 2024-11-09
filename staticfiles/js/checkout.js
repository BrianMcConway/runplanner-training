document.addEventListener("DOMContentLoaded", function () {
    // Retrieve public key
    const stripePublicKeyElement = document.getElementById("id_stripe_public_key");

    if (!stripePublicKeyElement) {
        console.error("Stripe public key element is missing.");
        document.getElementById("card-errors").textContent = "Payment setup error. Please try again later.";
        return;
    }

    const stripePublicKey = stripePublicKeyElement.textContent.trim();

    // Check if public key is available
    if (!stripePublicKey) {
        console.error("Stripe public key is missing.");
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

        // Collect form data
        const formData = new FormData(form);

        // Send form data to server to create the order and get client_secret and order_id
        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Order creation error:", data.error);
                    document.getElementById("card-errors").textContent = data.error;
                    document.getElementById("submit-button").disabled = false;
                } else {
                    const clientSecret = data.client_secret;
                    const orderId = data.order_id;

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
                                    state: form.county.value,
                                    postal_code: form.postcode.value,
                                    country: form.country.value,
                                },
                            },
                        },
                    }).then(function (result) {
                        if (result.error) {
                            console.error("Payment error:", result.error.message);
                            document.getElementById("card-errors").textContent = result.error.message;
                            document.getElementById("submit-button").disabled = false;
                        } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                            console.log("Payment succeeded, redirecting to success page.");

                            // Redirect to the order success page using the orderId
                            const orderSuccessUrl = `/checkout_v2/order_success/${orderId}/`;
                            window.location.href = orderSuccessUrl;
                        }
                    });
                }
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementById("card-errors").textContent = "An error occurred. Please try again.";
                document.getElementById("submit-button").disabled = false;
            });
    });
});
