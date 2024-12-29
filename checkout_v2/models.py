from django.db import models
from django_countries.fields import CountryField
from products_v2.models import Product


class Order(models.Model):
    """
    Model representing an order placed by a user.
    """
    full_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )  # Full name of the user placing the order
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False
    )  # Email address of the user
    phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )  # Contact number for the order
    country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False
    )  # Country of the user
    postcode = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )  # Optional postal code
    town_or_city = models.CharField(
        max_length=40,
        null=False,
        blank=False
    )  # Town or city name
    street_address1 = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )  # Primary street address
    street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )  # Optional secondary street address
    county = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )  # Optional county/state/region
    date = models.DateTimeField(
        auto_now_add=True
    )  # Date and time when the order was placed
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )  # Total cost of all items in the order
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )  # Final total after taxes and discounts
    original_basket = models.TextField(
        null=False,
        blank=False,
        default=''
    )  # JSON representation of the original basket
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        unique=True
    )  # Stripe PaymentIntent ID for tracking
    is_paid = models.BooleanField(
        default=False
    )  # Status indicating whether the order is paid

    def __str__(self):
        """
        String representation of the order.
        """
        return f"Order #{self.id}"


class OrderLineItem(models.Model):
    """
    Model representing an individual line item in an order.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )  # Link to the parent order
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )  # Product associated with the line item
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )  # Quantity of the product ordered
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )  # Total cost for this line item

    def save(self, *args, **kwargs):
        """
        Override save method to calculate line item total, update order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
