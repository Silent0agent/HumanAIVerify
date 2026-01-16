__all__ = ()

import bleach
from bleach.css_sanitizer import CSSSanitizer
from django.conf import settings


def sanitize_html(html_content):
    if not html_content:
        return ''

    css_sanitizer = CSSSanitizer(
        allowed_css_properties=settings.BLEACH_ALLOWED_CSS_PROPERTIES,
    )

    return bleach.clean(
        html_content,
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
        strip=settings.BLEACH_STRIP,
        css_sanitizer=css_sanitizer,
    )
