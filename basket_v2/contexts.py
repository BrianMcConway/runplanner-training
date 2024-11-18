from decimal import Decimal
from django.conf import settings
from .models import BasketItem


def basket_contents(request):
    """
    Retrieve the basket items and total cost, combining session and user items.
    """
    basket = request.session.get('basket', {})
    basket_items = []
    total = Decimal(0)

    # Load basket items from session
    for item in basket.values():
        total += Decimal(item['price']) * item['quantity']
        basket_items.append({
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'slug': item['slug'],
            'total_price': Decimal(item['price']) * item['quantity'],
        })

    # If user is authenticated, load basket items from the database
    if request.user.is_authenticated:
        user_basket_items = BasketItem.objects.filter(user=request.user)
        for item in user_basket_items:
            total += item.product.price * item.quantity
            basket_items.append({
                'name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.product.price),
                'slug': item.product.slug,
                'total_price': item.product.price * item.quantity,
            })

    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': total,  # Update if additional fees are added
    }

    return context