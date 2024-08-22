"""
Django settings for contest_service project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3&uwud=s#&0(uz**lf5$fi+m#)gf40l+s!v84l&afvi5bxqjr!'

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
    "api"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contest_service.urls'

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

WSGI_APPLICATION = 'contest_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "local": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "contest_db",
        "USER": os.environ.get("PG_USER") or "pguser",
        "PASSWORD": os.environ.get("PG_PASS") or "pgpass",
        "HOST": "localhost",
        "PORT": "5501",
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "contest_db",
        "USER": os.environ.get("PG_USER"),
        "PASSWORD": os.environ.get("PG_PASS"),
        "HOST": os.environ.get("PG_HOST"),
        "PORT": os.environ.get("PG_PORT"),
    }
}
DATABASES["default"] = DATABASES[MODE]

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
REST_FRAMEWORK = {
    # 'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "api.auth.RemoteAuthentication",
    )
}
ACCOUNT_SERVICE = os.getenv("ACCOUNT_SERVICE") or "http://localhost:8001/api/accounts"

RMQ_ADDRESS = os.getenv("RMQ_ADDRESS") or "localhost"
RMQ_USER = os.getenv("RMQ_USER") or "rm_user"
RMQ_PASS = os.getenv("RMQ_PASS") or "rm_password"
ENCODING = os.getenv("ENCODING") or "utf-8"
