import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import environ

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DJANGO_SECRET_KEY=(str, "1234"),
    DJANGO_DEBUG=(str, "false"),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    DJANGO_DEFAULT_USER_IS_ACTIVE=(bool, None),
    DJANGO_MAX_AUTH_ATTEMPTS=(int, 6),
    DJANGO_EMAIL_HOST=(str, "smtp.mail.ru"),
    DJANGO_DEFAULT_FROM_EMAIL=(str, "webmaster@localhost"),
)
environ.Env.read_env(os.path.join(PROJECT_ROOT, ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG").lower() in {"", "1", "on", "t", "true", "y", "yes"}

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

DEFAULT_USER_IS_ACTIVE = env("DJANGO_DEFAULT_USER_IS_ACTIVE", default=DEBUG)

MAX_AUTH_ATTEMPTS = env("DJANGO_MAX_AUTH_ATTEMPTS")

EMAIL_HOST = env("DJANGO_EMAIL_HOST")

DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "about.apps.AboutConfig",
    "core.apps.CoreConfig",
    "homepage.apps.HomepageConfig",
    "tasks.apps.TasksConfig",
    "users.apps.UsersConfig",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_USER_MODEL = "users.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "users.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = reverse_lazy("users:login")
LOGIN_REDIRECT_URL = reverse_lazy("users:profile")
LOGOUT_REDIRECT_URL = reverse_lazy("users:logout")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]
STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
