from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Pantalla de selección + registro
    path('', include('accounts.urls')),

    # Sistema de reportes
    path('reporte/', include('reporte.urls')),

    # Login y logout
    path('accounts/', include('django.contrib.auth.urls')),

    # Recuperación por código
    path('usuarios/', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)