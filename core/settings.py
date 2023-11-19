import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, "core/.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    # 3rd party app that needs to be before django.contrib.admin
    "django_admin_env_notice",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # local apps
    "apps.garage",
    "apps.rides",
    "apps.dashboard",
    "apps.kudos",
    "apps.trophies",
    "apps.hp",
    "apps.feed",
    "apps.pages",
    "apps.habits",
    # 3rd party apps
    "admin_honeypot",
    "django_bootstrap5",
    "bootstrap_datepicker_plus",
    "ckeditor",
    "django_seed",
    "django_htmx",
    "import_export",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # third-party additions
    "django_auto_logout.middleware.auto_logout",  # django-auto-logout
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # third-party additions
                "django_auto_logout.context_processors.auto_logout_client",  # django-auto-logout
                "django_admin_env_notice.context_processors.from_settings",  # django-admin-env-notice
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django_project/settings.py
LOGIN_REDIRECT_URL = "feed:feed"
LOGOUT_REDIRECT_URL = "landing"
LOGIN_URL = "login"


# Temp email solution, just writes emails to console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Temp SMTP email solution
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")

ADMIN_EMAIL = "admin@justtim.com"


# Configure CKEditor Toolbars
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            {
                "name": "group1",
                "items": [
                    "Format",
                    "Font",
                    "FontSize",
                ],
            },
            {
                "name": "group2",
                "items": [
                    "-",
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "TextColor",
                    "BGColor",
                    "-",
                    "Link",
                    "Image",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "Blockquote",
                    "-",
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                ],
            },
            {"name": "group2", "items": ["Undo", "Redo"]},
        ],
    },
}

# django-auto-logout settings
IDLE_TIME_MIN = int(env("IDLE_TIME_MIN"))
AUTO_LOGOUT = {
    "IDLE_TIME": timedelta(minutes=IDLE_TIME_MIN),
    "REDIRECT_TO_LOGIN_IMMEDIATELY": True,
    "MESSAGE": "The session has expired. Please login again to continue.",
}

# django-admin-env-notice settings
ENVIRONMENT_NAME = env("ENVIRONMENT_NAME")
ENVIRONMENT_COLOR = env("ENVIRONMENT_COLOR")
ENVIRONMENT_SHOW_TO_UNAUTHENTICATED = False


try:
    from .prod_settings import *
except ImportError:
    pass
