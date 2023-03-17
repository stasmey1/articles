from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from django.contrib.auth.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
