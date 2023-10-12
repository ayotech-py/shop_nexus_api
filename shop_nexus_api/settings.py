"""
Django settings for shop_nexus_api project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import cloudinary
import cloudinary.api
import cloudinary.uploader

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4$yqmb^rvxx-juvsgph#c52g2b!hsrgly)$0=2(=dtg4e5c5@a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Access-Control-Allow-Origin",
    "user",
]

CORS_ALLOWED_ORIGINS = [
    "https://ayotech-py.github.io",
    "http://localhost:8080",
    "http://0.0.0.0:8000",
    "http://localhost:3000",
]

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop_nexus_api_point",
    "rest_framework",
    "corsheaders",
    'cloudinary_storage',
    'cloudinary'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop_nexus_api.urls"

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

WSGI_APPLICATION = "shop_nexus_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """

""" DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "shopnexus",
        "USER": "root",
        "PASSWORD": "mysqlpassword",
        "HOST": "localhost",
        "PORT": "3306",
    }
} """

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "verceldb",
        "USER": "default",
        "PASSWORD": "4ofEQw9MVugO",
        "HOST": "ep-cold-frost-869893-pooler.us-east-1.postgres.vercel-storage.com",
    }
}

""" DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "aaayotech$shopnexus",
        "USER": "aaayotech",
        "PASSWORD": "mysqlpassword",
        "HOST": "aaayotech.mysql.pythonanywhere-services.com",
    }
} """

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

""" STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static") """

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "shop_media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "/tmp/media")
MEDIA_ROOT = os.path.join(BASE_DIR, "shop_media")

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

load_dotenv(find_dotenv())

# PAYSTACK_SECRET_KEY = os.environ["PAYSTACK_SECRET_KEY"]
# PAYSTACK_PUBLIC_KEY = os.environ["PAYSTACK_PUBLIC_KEY"]

PAYSTACK_SECRET_KEY = "sk_test_edb461d647e154482937cad0fbf5f619c2c142d7"
PAYSTACK_PUBLIC_KEY = "pk_test_80be5fa45cd9c618ea398bd079f47b5f974d938c"

CLOUD_NAME = os.environ["CLOUD_NAME"]
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']


CLOUDINARY_STORAGE = {
    "CLOUD_NAME" : CLOUD_NAME, 
    "API_KEY" : API_KEY, 
    "API_SECRET" : API_SECRET
}