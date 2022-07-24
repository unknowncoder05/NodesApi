from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/', include('api.users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
