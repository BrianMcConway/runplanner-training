from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from pages.views import robots_txt
from pages.sitemaps import StaticViewSitemap

# Sitemaps
sitemaps = {
    'static': StaticViewSitemap,  # Sitemap for static pages
}

urlpatterns = [
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # Main app URLs
    path('', include('home.urls')),
    path('products_v2/', include('products_v2.urls', namespace='products_v2')),
    path('basket_v2/', include('basket_v2.urls', namespace='basket_v2')),
    path('checkout_v2/', include('checkout_v2.urls', namespace='checkout_v2')),
    path('contact/', include('contact.urls')),
    path('my_account/', include('my_account.urls')),
    path('pages/', include('pages.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

    # Robots.txt and Sitemap
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # Password management
    path('accounts/', include('django.contrib.auth.urls')),

    # Markdown support
    path('markdownx/', include('markdownx.urls')),
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
