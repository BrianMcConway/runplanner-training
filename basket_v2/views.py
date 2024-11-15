from django.shortcuts import render, redirect, get_object_or_404
from products_v2.models import Product
from .models import BasketItem

class Basket:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        self.basket = self.session.get('basket', {})

    def add(self, product, quantity=1):
        product_slug = str(product.slug)

        if self.user.is_authenticated:
            # Save or update the item in the database for authenticated users
            basket_item, created = BasketItem.objects.get_or_create(
                user=self.user, product=product
            )
            if not created:
                basket_item.quantity += quantity
            basket_item.save()
        else:
            # Save to session for unauthenticated users
            if product_slug not in self.basket:
                self.basket[product_slug] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': quantity,
                    'slug': product_slug,
                }
            else:
                self.basket[product_slug]['quantity'] += quantity
            self.save()

    def save(self):
        """Mark the session as modified to ensure data is saved."""
        self.session['basket'] = self.basket
        self.session.modified = True

    def remove(self, product_slug):
        if self.user.is_authenticated:
            # Remove from the database if the user is authenticated
            BasketItem.objects.filter(user=self.user, product__slug=product_slug).delete()
        else:
            # Remove from session if not authenticated
            if product_slug in self.basket:
                del self.basket[product_slug]
                self.save()

    def get_items(self):
        items = []
        if self.user.is_authenticated:
            # Load items from the database for authenticated users
            user_items = BasketItem.objects.filter(user=self.user)
            for item in user_items:
                items.append({
                    'name': item.product.name,
                    'price': str(item.product.price),
                    'quantity': item.quantity,
                    'slug': item.product.slug,
                })
        else:
            # Load items from the session for unauthenticated users
            items = self.basket.values()
        return items

    def get_total_price(self):
        total = 0
        if self.user.is_authenticated:
            # Calculate total for authenticated users
            total = sum(item.product.price * item.quantity for item in BasketItem.objects.filter(user=self.user))
        else:
            # Calculate total for session items
            total = sum(float(item['price']) * item['quantity'] for item in self.basket.values())
        return total

    def clear(self):
        if self.user.is_authenticated:
            # Clear database basket items for authenticated users
            BasketItem.objects.filter(user=self.user).delete()
        else:
            # Clear session basket for unauthenticated users
            self.session['basket'] = {}
            self.save()


def add_to_basket(request, slug):
    """View to add a product to the basket."""
    product = get_object_or_404(Product, slug=slug)
    basket = Basket(request)
    basket.add(product)
    return redirect('basket_v2:show_basket')


def remove_from_basket(request, slug):
    """View to remove a product from the basket."""
    basket = Basket(request)
    basket.remove(slug)
    return redirect('basket_v2:show_basket')


def show_basket(request):
    """View to display all items in the basket."""
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
