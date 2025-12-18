__all__ = ()

import django.views.generic.base


class IndexView(django.views.generic.base.TemplateView):
    template_name = "homepage/index.html"
