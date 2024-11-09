# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products_v2/', include('products_v2.urls', namespace='products_v2')),
    path('basket_v2/', include('basket_v2.urls', namespace='basket_v2')),
    path('checkout_v2/', include('checkout_v2.urls', namespace='checkout_v2')),
    path('contact/', include('contact.urls')),
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
