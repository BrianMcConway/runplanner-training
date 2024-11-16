from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Post(models.Model):
    """Model for blog posts."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest posts first

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def get_content_as_markdown(self):
        """
        Convert the Markdown content to HTML, with sanitization.
        """
        from .utils import sanitize_markdown  # Import here to avoid circular imports
        return sanitize_markdown(self.content)

    def save(self, *args, **kwargs):
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
    """Model for comments on posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f'Comment by {self.commenter.username} on {self.post.title}'
