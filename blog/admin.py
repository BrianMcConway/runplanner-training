from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commenter', 'created_at')
    list_filter = ('commenter', 'created_at')
    search_fields = ('content',)
    ordering = ('created_at',)