import os

from .base import *  # noqa: F401, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "188.166.57.233",
    "dev.la-plateforme-a-caractere-associatif.org/",
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}


INSTALLED_APPS += [  # noqa: F405
    # https://django-extensions.readthedocs.io/en/latest/
    "django_extensions",
    # https://django-debug-toolbar.readthedocs.io/en/latest/index.html
    "debug_toolbar",
]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"  # noqa: F405
