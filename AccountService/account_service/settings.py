"""
Django settings for account_service project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import logging
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or 'django-insecure-e!dhn4o+qii7k+^sj&!2t(!1!su4=9ly#hh@h3$m06qhp&98$5'

# SECURITY WARNING: don't run with debug turned on in production!
MODE = os.getenv("MODE") or "local"

DEBUG = MODE == "local"

ALLOWED_HOSTS = []
if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    "rest_framework",
    "api"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #"corsheaders.middleware.CorsMiddleware",
    "api.middleware.SyncCorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'account_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'account_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "local": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "account_db",
        "USER": os.environ.get("PG_USER") or "pguser",
        "PASSWORD": os.environ.get("PG_PASS") or "pgpass",
        "HOST": "localhost",
        "PORT": "5432",
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "account_db",
        "USER": os.environ.get("PG_USER"),
        "PASSWORD": os.environ.get("PG_PASS"),
        "HOST": os.environ.get("PG_HOST"),
        "PORT": os.environ.get("PG_PORT"),
    }
}
DATABASES["default"] = DATABASES[MODE]
logging.info(f"Using database {DATABASES[MODE]['USER']}@"
             f"{DATABASES[MODE]['HOST']}/"
             f"{DATABASES[MODE]['NAME']}")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "AUTH_TOKEN_CLASSES": ("api.authentication.TokenWithInvalidation",),
}

RMQ_ADDRESS = os.getenv("RMQ_ADDRESS") or "localhost"
RMQ_USER = os.getenv("RMQ_USER") or "rm_user"
RMQ_PASS = os.getenv("RMQ_PASS") or "rm_password"
ENCODING = os.getenv("ENCODING") or "utf-8"

CORS_ALLOW_ALL_ORIGINS = True

ALLOW_REGISTRATION = str(os.getenv("ALLOW_REGISTRATION")).lower() != "false"
print(ALLOW_REGISTRATION, os.getenv("ALLOW_REGISTRATION"))
