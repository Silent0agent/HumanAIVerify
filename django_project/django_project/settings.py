from pathlib import Path

import bleach
import dj_database_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import environ

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DJANGO_ALLOWED_HOSTS=(list, ['*']),
    DJANGO_DATABASE_URL=(str, 'not_so_secret'),
    DJANGO_DEBUG=(str, 'false'),
    DJANGO_EMAIL_FROM_DEFAULT=(str, 'sender@mail'),
    DJANGO_DEFAULT_USER_IS_ACTIVE=(bool, None),
    DJANGO_EMAIL_BACKEND=(str, 'mailer.backend.DbBackend'),
    DJANGO_EMAIL_HOST=(str, 'localhost'),
    DJANGO_EMAIL_HOST_PASSWORD=(str, 'not_so_secret'),
    DJANGO_EMAIL_HOST_USER=(str, 'user@example.com'),
    DJANGO_EMAIL_PORT=(int, 0),
    DJANGO_EMAIL_USE_SSL=(bool, False),
    DJANGO_EMAIL_USE_TLS=(bool, False),
    DJANGO_MAILER_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_MAX_AUTH_ATTEMPTS=(int, 6),
    DJANGO_PROJECT_ABSOLUTE_PATH=(str, 'C://'),
    DJANGO_SECRET_KEY=(str, '1234'),
    DJANGO_TRAINING_COMPLETIONS_FOR_PERFORMER=(int, 10),
    DJANGO_UUID=(str, 'a-random-version-4-uuid'),
)
environ.Env.read_env(PROJECT_ROOT / '.env')

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS')

DJANGO_DATABASE_URL = env('DJANGO_DATABASE_URL')

DEBUG = env('DJANGO_DEBUG').lower() in {'', '1', 'on', 't', 'true', 'y', 'yes'}

SERVER_EMAIL = EMAIL_FROM_DEFAULT = env('DJANGO_EMAIL_FROM_DEFAULT')

DEFAULT_USER_IS_ACTIVE = env('DJANGO_DEFAULT_USER_IS_ACTIVE', default=DEBUG)

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND')
EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_PORT = env('DJANGO_EMAIL_PORT')
EMAIL_TIMEOUT = 15
EMAIL_USE_SSL = env('DJANGO_EMAIL_USE_SSL')
EMAIL_USE_TLS = env('DJANGO_EMAIL_USE_TLS')

MAILER_EMAIL_BACKEND = env('DJANGO_MAILER_EMAIL_BACKEND')
MAX_AUTH_ATTEMPTS = env('DJANGO_MAX_AUTH_ATTEMPTS')

PROJECT_ABSOLUTE_PATH = env('DJANGO_PROJECT_ABSOLUTE_PATH')

SECRET_KEY = env('DJANGO_SECRET_KEY')

TRAINING_COMPLETIONS_FOR_PERFORMER = env(
    'DJANGO_TRAINING_COMPLETIONS_FOR_PERFORMER',
)

UUID = env('DJANGO_UUID')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    # third-party apps
    'django_ckeditor_5',
    'mailer',
    'sorl.thumbnail',
    'tz_detect',
    # site apps
    'about.apps.AboutConfig',
    'core.apps.CoreConfig',
    'feedback.apps.FeedbackConfig',
    'homepage.apps.HomepageConfig',
    'tasks.apps.TasksConfig',
    'training.apps.TrainingConfig',
    'users.apps.UsersConfig',
    # system / cleanup
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = [
        '127.0.0.1',
    ]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DATABASES = {
    'default': (
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
        if DEBUG
        else dj_database_url.parse(
            DJANGO_DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_FILE_PATH = BASE_DIR / 'send_mail'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LOGIN_REDIRECT_URL = reverse_lazy('users:profile')
LOGIN_URL = reverse_lazy('auth:login')
LOGOUT_REDIRECT_URL = reverse_lazy('auth:logout')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

PERFORMER_GROUP_NAME = 'Performers'

ROOT_URLCONF = 'django_project.urls'

STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

WSGI_APPLICATION = 'django_project.wsgi.application'

# ckeditor
CUSTOM_COLOR_PALETTE = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

CKEDITOR_5_CUSTOM_CSS = 'css/custom_ckeditor5.css'
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'any'
CKEDITOR_5_CONFIGS = {
    'create_text_task_content': {
        'blockToolbar': [
            'paragraph',
            'heading1',
            'heading2',
            'heading3',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative',
                'imageStyle:inline',
                'imageStyle:block',
                'imageStyle:side',
                'imageStyle:alignLeft',
                'imageStyle:alignCenter',
                'imageStyle:alignRight',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
        },
        'toolbar': {
            'items': [
                'heading',
                '|',
                'outdent',
                'indent',
                '|',
                'bold',
                'italic',
                'link',
                'underline',
                'strikethrough',
                'code',
                'subscript',
                'superscript',
                'highlight',
                '|',
                'bulletedList',
                'numberedList',
                'todoList',
                '|',
                'blockQuote',
                '|',
                'fontSize',
                'fontFamily',
                'fontColor',
                'fontBackgroundColor',
                'removeFormat',
                'insertTable',
            ],
            'shouldNotGroupWhenFull': 'true',
        },
        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties',
            ],
            'tableProperties': {
                'borderColors': CUSTOM_COLOR_PALETTE,
                'backgroundColors': CUSTOM_COLOR_PALETTE,
            },
            'tableCellProperties': {
                'borderColors': CUSTOM_COLOR_PALETTE,
                'backgroundColors': CUSTOM_COLOR_PALETTE,
            },
        },
        'heading': {
            'options': [
                {
                    'model': 'paragraph',
                    'title': 'Paragraph',
                    'class': 'ck-heading_paragraph',
                },
                {
                    'model': 'heading1',
                    'view': 'h1',
                    'title': 'Heading 1',
                    'class': 'ck-heading_heading1',
                },
                {
                    'model': 'heading2',
                    'view': 'h2',
                    'title': 'Heading 2',
                    'class': 'ck-heading_heading2',
                },
                {
                    'model': 'heading3',
                    'view': 'h3',
                    'title': 'Heading 3',
                    'class': 'ck-heading_heading3',
                },
            ],
        },
    },
}

BLEACH_ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    'p',
    'div',
    'span',
    'br',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'b',
    'i',
    'strong',
    'em',
    'u',
    'img',
    'blockquote',
    'ul',
    'ol',
    'li',
]

BLEACH_ALLOWED_ATTRIBUTES = {
    '*': ['style'],
    'span': ['class'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
}

BLEACH_ALLOWED_CSS_PROPERTIES = [
    'color',
    'background-color',
    'font-family',
    'font-size',
    'font-weight',
    'font-style',
    'text-decoration',
    'text-align',
    'vertical-align',
    'width',
    'height',
    'min-width',
    'max-width',
    'margin',
    'margin-top',
    'margin-bottom',
    'margin-left',
    'margin-right',
    'padding',
    'padding-top',
    'padding-bottom',
    'padding-left',
    'padding-right',
    'border',
    'border-width',
    'border-style',
    'border-color',
    'float',
]

BLEACH_STRIP = True
