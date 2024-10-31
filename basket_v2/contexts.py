# basket_v2/contexts.py

from decimal import Decimal
from django.conf import settings

def basket_contents(request):
    """
    Retrieve the basket items and total cost.
    """
    basket = request.session.get('basket', {})
    basket_items = []
    total = Decimal(0)

    for item in basket.values():
        total += Decimal(item['price']) * item['quantity']
        basket_items.append({
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'slug': item['slug'],
            'total_price': Decimal(item['price']) * item['quantity']
        })

    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': total  # Update if additional fees (e.g., shipping) are added
    }

    return context
