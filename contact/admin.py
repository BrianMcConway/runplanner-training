from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing ContactMessage records.
    """

    # Fields to display in the admin list view
    list_display = ('name', 'email', 'subject', 'created_at')

    # Fields to include in the admin search bar
    search_fields = ('name', 'email', 'subject')
