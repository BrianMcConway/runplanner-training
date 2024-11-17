from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "weekly"  # How often the page is updated
    priority = 0.8         # Priority for crawling (1.0 is highest)

    def items(self):
        return Post.objects.filter(is_published=True)  # Query for blog posts

    def lastmod(self, obj):
        return obj.updated_at  # Use the post's last updated timestamp

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['home', 'contact:contact', 'pages:about']  # Named URL patterns

    def location(self, item):
        return reverse(item)  # Generate URLs from patterns
