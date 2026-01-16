__all__ = ()

import django.urls

import homepage.views


app_name = 'homepage'

urlpatterns = [
    django.urls.path('', homepage.views.IndexView.as_view(), name='index'),
    django.urls.path(
        '.well-known/appspecific/com.chrome.devtools.json/',
        homepage.views.ChromeDevtools.as_view(),
        name='chrome_devtools',
    ),
]
