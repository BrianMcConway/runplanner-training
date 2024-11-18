from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import BasketItem
from products_v2.models import Product
from .views import Basket


@receiver(user_logged_in)
def sync_basket_on_login(sender, request, user, **kwargs):
    """
    Syncs session basket to persistent basket on login.
    """
    session_basket = Basket(request)

    # Transfer session basket items to the user's persistent basket
    for item in session_basket.get_items():
        product_slug = item['slug']
        quantity = item['quantity']
        product = Product.objects.get(slug=product_slug)

        # Update or create BasketItem
        BasketItem.objects.update_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity},
        )

    # Clear session basket after sync to avoid duplication
    session_basket.clear()
    request.session.modified = True
