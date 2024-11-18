from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products_v2.models import Product
from .models import BasketItem


class Basket:
    """
    A class to manage basket operations for both authenticated
    and unauthenticated users.
    """
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        self.basket = self.session.get('basket', {})

    def add(self, product, quantity=1):
        """
        Add a product to the basket or update its quantity.
        """
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
        """
        Mark the session as modified to ensure data is saved.
        """
        self.session['basket'] = self.basket
        self.session.modified = True

    def remove(self, product_slug):
        """
        Remove a product from the basket.
        """
        if self.user.is_authenticated:
            BasketItem.objects.filter(
                user=self.user, product__slug=product_slug
            ).delete()
        else:
            if product_slug in self.basket:
                del self.basket[product_slug]
                self.save()

    def get_items(self):
        """
        Retrieve all items in the basket.
        """
        items = []
        if self.user.is_authenticated:
            user_items = BasketItem.objects.filter(user=self.user)
            for item in user_items:
                items.append({
                    'name': item.product.name,
                    'price': str(item.product.price),
                    'quantity': item.quantity,
                    'slug': item.product.slug,
                })
        else:
            items = self.basket.values()
        return items

    def get_total_price(self):
        """
        Calculate the total price of all items in the basket.
        """
        if self.user.is_authenticated:
            return sum(
                item.product.price * item.quantity
                for item in BasketItem.objects.filter(user=self.user)
            )
        return sum(
            float(item['price']) * item['quantity']
            for item in self.basket.values()
        )

    def clear(self):
        """
        Clear all items from the basket.
        """
        if self.user.is_authenticated:
            BasketItem.objects.filter(user=self.user).delete()
        else:
            self.session['basket'] = {}
            self.save()


def add_to_basket(request, slug):
    """
    View to add a product to the basket.
    """
    product = get_object_or_404(Product, slug=slug)
    basket = Basket(request)
    basket.add(product)

    messages.success(
        request,
        f"'{product.name}' has been added to your basket!"
    )
    return redirect('basket_v2:show_basket')


def remove_from_basket(request, slug):
    """
    View to remove a product from the basket.
    """
    product = get_object_or_404(Product, slug=slug)
    basket = Basket(request)
    basket.remove(slug)

    messages.warning(
        request,
        f"'{product.name}' has been removed from your basket."
    )
    return redirect('basket_v2:show_basket')


def show_basket(request):
    """
    View to display all items in the basket.
    """
    basket = Basket(request)
    items = basket.get_items()
    total_price = basket.get_total_price()

    if not items:
        messages.info(request, "Your basket is currently empty.")

    return render(request, 'basket_v2/basket.html', {
        'basket': items,
        'total_price': total_price,
    })


def clear_basket(request):
    """
    View to clear the entire basket.
    """
    basket = Basket(request)
    basket.clear()

    messages.info(request, "Your basket has been cleared.")
    return redirect('basket_v2:show_basket')
