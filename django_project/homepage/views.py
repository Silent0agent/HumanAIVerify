__all__ = ()

import django.conf
import django.http
import django.views.generic.base


class IndexView(django.views.generic.base.TemplateView):
    template_name = 'homepage/index.html'


class ChromeDevtools(django.views.generic.base.View):
    def get(self, request):
        return django.http.JsonResponse(
            {
                'workspace': {
                    'root': django.conf.settings.PROJECT_ABSOLUTE_PATH,
                    'uuid': django.conf.settings.UUID,
                },
            },
        )
