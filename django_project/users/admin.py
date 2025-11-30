__all__ = ()

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import GroupProxy

User = auth.get_user_model()


@admin.register(User)
class CustomUserAdmin(auth.admin.UserAdmin):
    avatar_field = User.avatar.field.name

    fieldsets = auth.admin.UserAdmin.fieldsets + (
        (_("Additional_information"), {"fields": (avatar_field,)}),
    )
    add_fieldsets = auth.admin.UserAdmin.add_fieldsets + (
        (None, {"fields": (avatar_field,)}),
    )


admin.site.unregister(Group)
admin.site.register(GroupProxy, GroupAdmin)
