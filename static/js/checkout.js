document.addEventListener("DOMContentLoaded", function () {
    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe public key or client secret is missing.");
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const card = elements.create('card', {
        style: {
            base: {
                color: "#32325d",
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: "antialiased",
                fontSize: "16px",
                "::placeholder": {
                    color: "#aab7c4"
                }
            },
            invalid: {
                color: "#fa755a",
                iconColor: "#fa755a"
            }
        },
        hidePostalCode: true
    });
    card.mount("#card-element");

    card.on("change", function(event) {
        const displayError = document.getElementById("card-errors");
        displayError.textContent = event.error ? event.error.message : "";
    });

    let checkoutInProgress = false;

    const form = document.getElementById("payment-form");
    const submitButton = document.getElementById("submit-button");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        if (checkoutInProgress) return;

        checkoutInProgress = true;
        submitButton.disabled = true;

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card
            }
        }).then(function(result) {
            if (result.error) {
                document.getElementById("card-errors").textContent = result.error.message;
                submitButton.disabled = false;
                checkoutInProgress = false;
            } else if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
                form.style.display = "none";
                document.getElementById("success-message").style.display = "block";
                document.getElementById("order-id").textContent = "{{ order_id }}";
            }
        });
    });
});
