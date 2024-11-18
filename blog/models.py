from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    """
    Model representing blog posts.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE  # Delete post if the author is deleted
    )
    title = models.CharField(
        max_length=200  # Title of the blog post
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        blank=True  # Auto-generated if left blank
    )
    content = MarkdownxField()  # Supports Markdown formatting
    created_at = models.DateTimeField(
        auto_now_add=True  # Automatically set on creation
    )
    updated_at = models.DateTimeField(
        auto_now=True  # Automatically set on each update
    )

    class Meta:
        ordering = ['-created_at']  # Order posts by newest first

    def __str__(self):
        """
        String representation of the post.
        """
        return self.title

    def get_absolute_url(self):
        """
        Return the URL to view this post.
        """
        return reverse('blog:post_detail', args=[self.slug])

    def get_content_as_markdown(self):
        """
        Convert Markdown content to sanitized HTML.
        """
        from .utils import sanitize_markdown  # To avoid circular imports
        return sanitize_markdown(self.content)

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate unique slugs.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Post.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f'{base_slug}-{n}'
                n += 1
            self.slug = slug
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    """
    Model representing comments on posts.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # Delete comment if the post is deleted
        related_name='comments'  # Allows reverse access to post.comments
    )
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE  # Delete comment if the user is deleted
    )
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(
        auto_now_add=True  # Automatically set on creation
    )

    class Meta:
        ordering = ['created_at']  # Order comments by oldest first

    def __str__(self):
        """
        String representation of the comment.
        """
        return f'Comment by {self.commenter.username} on {self.post.title}'