from django.contrib import admin
from django.urls import path, include

# Media Files Configuration
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Trikha Store Admin Panel'
admin.site.index_title = 'Trikha Store Main Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('playground.urls')),
    path('store/', include('store.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)