from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from basket_v2.models import BasketItem
from products_v2.models import Product

@receiver(user_logged_in)
def merge_basket_on_login(request, user, **kwargs):
    session_basket = request.session.get('basket', {})
    for product_slug, item_data in session_basket.items():
        try:
            product = Product.objects.get(slug=product_slug)
            quantity = item_data.get('quantity', 1)
            basket_item, created = BasketItem.objects.get_or_create(user=user, product=product)
            if not created:
                basket_item.quantity += quantity
            else:
                basket_item.quantity = quantity
            basket_item.save()
        except Product.DoesNotExist:
            continue
    # Clear session basket after merging
    request.session['basket'] = {}