"""
Django settings for androxine project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import logging

from pathlib import Path

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'some secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

FRONTEND_PROTOCOL = 'https' if bool(
    int(os.environ.get('FRONTEND_IS_SECURE', 0))) else 'http'
FRONTEND_DOMAIN = os.environ.get('FRONTEND_DOMAIN', '127.0.0.1')
FRONTEND_PORT = os.environ.get('FRONTEND_PORT', 80)
FRONTEND_URL = '{}://{}:{}'.format(
    FRONTEND_PROTOCOL,
    FRONTEND_DOMAIN,
    FRONTEND_PORT
)

ALLOWED_HOSTS = [FRONTEND_DOMAIN]
CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'social_django',            # auth through OAuth2
    'django_elasticsearch_dsl',  # elasticsearch
    'drf_yasg',                 # swagger auto documentation
    'corsheaders',

    'authenticate',
    'exercise',
    'workout_template',
    'workout_settings',
    'weight',
    'calculator',
    'workout',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'config.middleware.DisableClientSideCachingMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.PageNumberTotalPagesPagination',
    'PAGE_SIZE': 25
}

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'authenticate.backends.EmailUsernameModelBackend',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR.parent / 'db.sqlite3'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


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

LOGLEVEL = logging.getLevelName(os.environ.get('LOGLEVEL', 'info').upper())

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 20 if LOGLEVEL < 20 else LOGLEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console']
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'django.utils.autoreload': {
            'level': 'WARNING',
            'handlers': ['console']
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authenticate.User'

LOGIN_URL = reverse_lazy('signin')

AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# Django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# SMTP Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Social OAuth2 pipelines
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Social OAuth2 Google settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get(
    'GOOGLE_OAUTH2_CLIENT_SECRET')

SOCIAL_AUTH_LOGIN_REDIRECT_URL = FRONTEND_URL + '/home'

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

# Elasticsearch settings
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT')
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://{}:{}'.format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
    },
}

SWAGGER_SETTINGS = {
    'LOGIN_URL': LOGIN_URL,
    'LOGOUT_URL': reverse_lazy('signout'),
    'SECURITY_DEFINITIONS': {
        'Your App API - Swagger': {
            'type': 'oauth2',
            'flow': 'accessCode',
            'authorizationUrl': reverse_lazy('social:begin', args=['google-oauth2']),
        },
    },
    'OAUTH2_REDIRECT_URL': 'http://localhost/static/drf-yasg/swagger-ui-dist/oauth2-redirect.html',
    'OAUTH2_CONFIG': {
        'clientId': os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'),
        'clientSecret': os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET'),
        'appName': 'google'
    },
}
