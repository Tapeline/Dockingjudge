import logging
import pprint
from datetime import timedelta
from pathlib import Path

from account_service.config import service_config_loader

logger = logging.getLogger(__name__)

config = service_config_loader.load()
logger.info("Config loaded %s", pprint.pformat(config))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config.security.secret_key
DEBUG = config.mode == "local"
ALLOWED_HOSTS = config.security.allowed_hosts

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    "django_prometheus",
    "api",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "api.middleware.SyncCorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "account_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "account_service.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "local": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config.postgres.database,
        "USER": config.postgres.username,
        "PASSWORD": config.postgres.password,
        "HOST": config.postgres.host,
        "PORT": str(config.postgres.port),
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config.postgres.database,
        "USER": config.postgres.username,
        "PASSWORD": config.postgres.password,
        "HOST": config.postgres.host,
        "PORT": str(config.postgres.port),
    },
}
DATABASES["default"] = DATABASES[config.mode]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "AUTH_TOKEN_CLASSES": ("api.authentication.TokenWithInvalidation",),
}

RMQ_ADDRESS = config.rabbit.host
RMQ_PORT = config.rabbit.port
RMQ_USER = config.rabbit.username
RMQ_PASS = config.rabbit.password
ENCODING = "utf-8"

ALLOW_REGISTRATION = config.app.allow_registration

SPECTACULAR_SETTINGS = {
    "TITLE": "Account Service API",
    "DESCRIPTION": "Account Service of Dockingjudge",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
