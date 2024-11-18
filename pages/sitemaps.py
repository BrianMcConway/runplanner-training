from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like Home, Contact, and About Us.
    """
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        # Return the named URL patterns for static pages
        return ['home', 'contact:contact', 'pages:about']

    def location(self, item):
        # Generate the URL for each named pattern
        return reverse(item)
