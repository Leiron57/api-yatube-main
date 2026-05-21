from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path  # noqa

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),  # noqa
    path('api/v1/api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),  # noqa
    path('auth/', include('djoser.urls.jwt')),  # noqa
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )