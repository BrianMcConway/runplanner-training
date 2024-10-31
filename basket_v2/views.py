# basket_v2/views.py

from django.shortcuts import render, redirect, get_object_or_404
from products_v2.models import Product  # Updated to use Product

# Create a simple basket class to interact with the session
class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if not basket:
            basket = self.session['basket'] = {}
        self.basket = basket

    def add(self, product, quantity=1):
        product_slug = str(product.slug)
        if product_slug not in self.basket:
            self.basket[product_slug] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'slug': product_slug,  # Ensure slug is saved
            }
        else:
            self.basket[product_slug]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_slug):
        if product_slug in self.basket:
            del self.basket[product_slug]
            self.save()

    def get_items(self):
        return self.basket.values()

    def get_total_price(self):
        total = sum(float(item['price']) * item['quantity'] for item in self.basket.values())
        return total

    def clear(self):
        """Clear the entire basket."""
        self.session['basket'] = {}
        self.save()


def add_to_basket(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Updated to use Product
    basket = Basket(request)
    basket.add(product)
    return redirect('basket_v2:show_basket')


def remove_from_basket(request, slug):
    basket = Basket(request)
    basket.remove(slug)
    return redirect('basket_v2:show_basket')


def show_basket(request):
    basket = Basket(request)
    items = basket.get_items()

    # Calculate total price for all items in the basket
    total_price = basket.get_total_price()

    return render(request, 'basket_v2/basket.html', {
        'basket': items,
        'total_price': total_price,
    })


def clear_basket(request):
    """View to clear the entire basket."""
    basket = Basket(request)
    basket.clear()
    return redirect('basket_v2:show_basket')
