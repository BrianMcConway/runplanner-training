from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from pages.views import robots_txt

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

    # Robots.txt
    path('robots.txt', robots_txt, name='robots_txt'),

    # Serve static sitemap.xml
    path(
        'sitemap.xml',
        serve,
        {'document_root': settings.STATIC_ROOT, 'path': 'sitemap.xml'},
        name='sitemap'
    ),

    # Markdown support
    path('markdownx/', include('markdownx.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )