__all__ = ()

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls.auth_urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('feedback/', include('feedback.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('tasks/', include('tasks.urls')),
    path('training/', include('training.urls')),
    path('tz_detect/', include('tz_detect.urls')),
    path('users/', include('users.urls.users_urls')),
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
    re_path(
        r'^static/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATIC_ROOT},
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += debug_toolbar.toolbar.debug_toolbar_urls()

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
