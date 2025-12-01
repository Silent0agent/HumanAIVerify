__all__ = ()

import re

from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def normalize_email(self, email):
        if not email or "@" not in email:
            return email

        email = super().normalize_email(email)
        email = email.lower()
        local_part, domain = email.split("@")

        local_part = local_part.split("+")[0]

        if domain in ["yandex.ru", "ya.ru"]:
            domain = "yandex.ru"
            local_part = local_part.replace(".", "-")
        elif domain == "gmail.com":
            local_part = local_part.replace(".", "")

        local_part = re.sub(r"\+.*", "", local_part)
        return f"{local_part}@{domain}"

    def by_mail(self, email):
        return self.filter(email=email).first()

    def public_information(self):
        return self.only(
            self.model.username.field.name,
            self.model.email.field.name,
            self.model.avatar.field.name,
        )
