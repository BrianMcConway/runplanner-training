from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # List all posts
    path('', views.post_list, name='post_list'),

    # Create a new post (admin only)
    path('post/new/', views.post_create, name='post_create'),

    # View details of a specific post by slug
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Edit a specific post by slug (admin only)
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    # Delete a specific post by slug (admin only)
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),

    # Edit a specific comment by primary key
    path(
        'comment/<int:pk>/edit/',
        views.comment_edit,
        name='comment_edit'
    ),

    # Delete a specific comment by primary key
    path(
        'comment/<int:pk>/delete/',
        views.comment_delete,
        name='comment_delete'
    ),
]
