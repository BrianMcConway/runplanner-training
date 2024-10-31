from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('date', 'order_total', 'grand_total', 'original_basket', 'stripe_pid')

    fields = ('full_name', 'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'date', 'order_total',
              'grand_total', 'original_basket', 'stripe_pid')

    list_display = ('id', 'full_name', 'date', 'order_total', 'grand_total')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
