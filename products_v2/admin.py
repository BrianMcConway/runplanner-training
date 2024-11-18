from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'slug', 'price',
        'distance', 'difficulty', 'terrain', 'elevation'
    )
    list_filter = (
        'category', 'distance', 'difficulty',
        'terrain', 'elevation'
    )
    prepopulated_fields = {'slug': ('name',)}
