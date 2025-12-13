__all__ = ()

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

import core.paginators
from users.models import GroupProxy

User = auth.get_user_model()


class AdminUserCreationForm(auth.forms.UserCreationForm):
    class Meta(auth.forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.email.field.name,
            User.username.field.name,
        )


@admin.register(User)
class CustomUserAdmin(auth.admin.UserAdmin):
    paginator = core.paginators.CountOptimizedPaginator
    show_full_result_count = False

    add_form = AdminUserCreationForm

    avatar_field = User.avatar.field.name
    role_field = User.role.field.name
    email_field = User.email.field.name
    username_field = User.username.field.name

    login_attempts_count_field = User.login_attempts_count.field.name
    block_time_field = User.block_timestamp.field.name
    last_login_attempt_field = User.last_login_attempt_timestamp.field.name

    last_login_field = User.last_login.field.name
    date_joined_field = User.date_joined.field.name
    first_name_field = User.first_name.field.name
    last_name_field = User.last_name.field.name
    is_staff_field = User.is_staff.field.name

    avatar_tmb_method = User.avatar_tmb.__name__

    list_display = (
        username_field,
        email_field,
        first_name_field,
        last_name_field,
        role_field,
        avatar_tmb_method,
        is_staff_field,
    )

    readonly_fields = (
        avatar_tmb_method,
        block_time_field,
        date_joined_field,
        last_login_attempt_field,
        last_login_field,
        login_attempts_count_field,
    )

    fieldsets = auth.admin.UserAdmin.fieldsets + (
        (
            _("security_profile"),
            {
                "fields": (
                    login_attempts_count_field,
                    block_time_field,
                    last_login_attempt_field,
                ),
            },
        ),
        (
            _("additional_information"),
            {
                "fields": (
                    role_field,
                    (avatar_field, "avatar_tmb"),
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    email_field,
                    username_field,
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.unregister(Group)
admin.site.register(GroupProxy, GroupAdmin)
