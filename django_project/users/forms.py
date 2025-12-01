__all__ = ()

from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import core.forms

User = auth.get_user_model()


class CustomAuthenticationForm(
    core.forms.BootstrapFormMixin,
    auth.forms.AuthenticationForm,
):
    remember_me = forms.BooleanField(required=False)
    username = forms.CharField(
        label=_("username_or_email_label"),
        max_length=254,
    )


class UserProfileForm(core.forms.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            User.avatar.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        ]


class SignUpForm(core.forms.BootstrapFormMixin, auth.forms.UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get(User.email.field.name)

        if email:
            normalized_email = User.objects.normalize_email(email)
            if User.objects.filter(email=normalized_email).exists():
                raise ValidationError(
                    _("User_with_this_email_already_exists"),
                )

        return email

    class Meta(auth.forms.UserCreationForm.Meta):
        model = User
        fields = [
            User.email.field.name,
            User.username.field.name,
            "password1",
            "password2",
        ]
