from django.contrib.auth.models import User
from django.db import models
from products_v2.models import Product


class BasketItem(models.Model):
    """
    Represents an item in a user's basket.
    """

    # The user who owns the basket item
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete basket items if the user is deleted
    )

    # The product added to the basket
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Remove items if the product is deleted
    )

    # Quantity of the product in the basket
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        """
        Meta options for the BasketItem model.
        """
        # Ensure each user-product combination is unique
        unique_together = ('user', 'product')

    def __str__(self):
        """
        String representation of the BasketItem model.
        """
        return f"{self.product.name} ({self.quantity})"
