"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e+-9bgh7k53efji#+9q1^i9j*=0d(k-%kx^-k4k5yyy4#@*agm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_email_verification",
    "mdeditor",
    
    "users.apps.UsersConfig",
    "notes.apps.NotesConfig",
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DB_USER = os.getenv("DB_USER")
DB_PASSWD = os.getenv("DB_PASSWD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_DATABASE,
        'HOST': DB_HOST,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWD,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [BASE_DIR / STATIC_URL]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / MEDIA_URL
MEDIAFILES_DIRS = [MEDIA_ROOT]

AUTH_USER_MODEL = "users.DiaryUser"
LOGOUT_REDIRECT_URL = "/profile/login"
LOGIN_REDIRECT_URL = "/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = "SAMEORIGIN"

MDEDITOR_CONFIGS = {
    'default':{
        'width': '100% ', 
        'height': 700, 
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"], 
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"], 
        'image_folder': 'static/images', 
        'theme': 'default',  
        'preview_theme': 'default', 
        'editor_theme': 'default',
        'toolbar_autofixed': True, 
        'search_replace': True,
        'emoji': False,  
        'tex': True,
        'flow_chart': True,
        'sequence': True, 
        'watch': False,
        'lineWrapping': True, 
        'lineNumbers': False, 
        'language': 'en' 
    }
    
}


def email_verified_callback(user):
    user.is_verified = True


def password_change_callback(user, new_password: Any | str):
    user.set_password(new_password)


TOKEN_LIFE = 60 * 1  # 1 minute

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

EMAIL_FROM_ADDRESS = EMAIL_HOST_USER
EMAIL_PAGE_DOMAIN = 'http://localhost:8000/'

EMAIL_MAIL_SUBJECT = 'Здравствуйте, {{ user.username }}, подтвердите свою почту'
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_MAIL_PLAIN = 'mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = TOKEN_LIFE 

EMAIL_MAIL_PAGE_TEMPLATE = 'email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

EMAIL_PASSWORD_SUBJECT = 'Здравствуйте, {{ user.username }}, измените свой пароль'
EMAIL_PASSWORD_HTML = 'password_body.html'
EMAIL_PASSWORD_PLAIN = 'password_body.txt'
EMAIL_PASSWORD_TOKEN_LIFE = TOKEN_LIFE

EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
EMAIL_PASSWORD_CALLBACK = password_change_callback


CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = TOKEN_LIFE
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_SERIALIZER = "json"
