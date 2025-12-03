__all__ = ()

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from tasks.models import TextTask


@admin.register(TextTask)
class TextTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("title", "content", "client__email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("client", "title", "content")}),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
