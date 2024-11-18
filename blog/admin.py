from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    """
    list_display = (
        'title', 'author', 'created_at', 'updated_at'
    )  # Fields displayed in the list view
    list_filter = (
        'author', 'created_at'
    )  # Filters for narrowing down posts in the admin
    search_fields = (
        'title', 'content'
    )  # Search functionality for title and content
    ordering = (
        '-created_at',
    )  # Default ordering by most recent posts
    prepopulated_fields = {
        'slug': ('title',)
    }  # Auto-generate slug based on title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    """
    list_display = (
        'post', 'commenter', 'created_at'
    )  # Fields displayed in the list view
    list_filter = (
        'commenter', 'created_at'
    )  # Filters for narrowing down comments in the admin
    search_fields = (
        'content',
    )  # Search functionality for content
    ordering = (
        'created_at',
    )  # Default ordering by oldest comments first
