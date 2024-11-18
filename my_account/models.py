from django.db import models
from django.contrib.auth.models import User
from products_v2.models import Product


class Purchase(models.Model):
    """
    Model to track purchases of training plans by users.
    """

    # The user who made the purchase
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE  # Delete purchase if the user is deleted
    )

    # The training plan purchased by the user
    training_plan = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Delete purchase if the product is deleted
        limit_choices_to={'category': 'training_plan'}  # Limit to plans
    )

    # Date and time when the purchase was made
    purchase_date = models.DateTimeField(
        auto_now_add=True
    )

    # Indicates whether the payment for this purchase is verified
    payment_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        """
        String representation of the Purchase model.
        """
        return f"{self.user.username} - {self.training_plan.title}"