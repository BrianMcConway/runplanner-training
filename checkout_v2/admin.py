from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin configuration for OrderLineItem.
    Allows managing line items directly within the Order admin interface.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)  # Fields that are read-only


class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Customization for the display and management of orders in the admin panel.
    """
    inlines = (OrderLineItemAdminInline,)  # Include OrderLineItem as inline

    readonly_fields = (
        'date', 'order_total', 'grand_total',
        'original_basket', 'stripe_pid'
    )  # Fields that are read-only in the admin

    fields = (
        'full_name', 'email', 'phone_number', 'country',
        'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county', 'date', 'order_total',
        'grand_total', 'original_basket', 'stripe_pid'
    )  # Fields to display in the admin form

    list_display = (
        'id', 'full_name', 'date',
        'order_total', 'grand_total'
    )  # Columns displayed in the orders list

    ordering = ('-date',)  # Order by date in descending order


# Register the Order model with the custom admin configuration
admin.site.register(Order, OrderAdmin)