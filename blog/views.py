from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings

def is_admin(user):
    return user.is_staff

def post_list(request):
    """View for listing all posts."""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    """View for a single post and its comments."""
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None

    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.commenter = request.user
                new_comment.save()
                messages.success(request, 'Your comment has been added.')
                return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, 'You need to be logged in to comment.')
            # Redirect to login with `next` parameter
            login_url = f"{settings.LOGIN_URL}?next={request.path}"
            return redirect(login_url)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })

@user_passes_test(is_admin)
def post_create(request):
    """View for creating a new post (admin only)."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Admin user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@user_passes_test(is_admin)
def post_edit(request, slug):
    """View for editing a post (admin only)."""
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('blog:post_detail', slug=post.slug)
    return render(request, 'blog/post_form.html', {'form': form})

@user_passes_test(is_admin)
def post_delete(request, slug):
    """View for confirming and deleting a post (admin only)."""
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        # Delete the post
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('blog:post_list')

    # If GET request, render confirmation page
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def comment_edit(request, pk):
    """View for editing a comment (comment owner only)."""
    comment = get_object_or_404(Comment, pk=pk, commenter=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Comment updated successfully.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_delete(request, pk):
    """View for confirming and deleting a comment (comment owner only)."""
    comment = get_object_or_404(Comment, pk=pk, commenter=request.user)

    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('blog:post_detail', slug=post_slug)

    # If GET request, render confirmation page
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
