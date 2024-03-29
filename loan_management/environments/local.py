"""
Django settings for Loan Management project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import random
import string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import dirname, abspath, basename
from logging import DEBUG as DEBUG_LOGGING
from corsheaders.defaults import default_headers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = "Loan Management"
SITE_ID = 1
SITE_URL = '192.168.33.66'
ALLOWED_HOSTS = ['*']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    with open(os.path.join(BASE_DIR, 'SECRET_KEY')) as f:
        SECRET_KEY = f.read().strip()
except FileNotFoundError:
    generated_key = ''.join(
        [random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)])
    secret = open(os.path.join(BASE_DIR, 'SECRET_KEY'), 'w')
    secret.write(generated_key)
    secret.close()
    SECRET_KEY = generated_key

# SECURITY WARNING: don't run with debug turned on in production!

try:
    with open(os.path.join(BASE_DIR, 'loan_management/DEBUG')) as f:
        _debug = f.read().strip()
        if _debug != "DO-NOT-USE-IN-PRODUCTION":
            DEBUG = False
        else:
            DEBUG = True
except FileNotFoundError:
    DEBUG = False

########################################################################################################################
# DEBUG TOOLBAR SETTINGS
########################################################################################################################
INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0',
]
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def show_toolbar(request):
    if DEBUG:
        return False
    return False


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar
}

########################################################################################################################
# LOGGING HANDA
########################################################################################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

########################################################################################################################
# MODEL SETTINGS
########################################################################################################################
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

########################################################################################################################
# USER MODEL
########################################################################################################################
AUTH_USER_MODEL = 'accounts.Account'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
TOKEN_LIFETIME = 21600  # 6 hours
# LOGIN_REDIRECT_URL = '/accounts/postlogin'

########################################################################################################################
# EMAIL
########################################################################################################################
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

########################################################################################################################
# DJANGO REST FRAMEWORK
########################################################################################################################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'ORDERING_PARAM': 'ordering',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # DEBUG
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'loan_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
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

WSGI_APPLICATION = 'loan_management.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'loan_management_db',
        'USER': 'loan_management_user',
        'PASSWORD': 'asdf1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

########################################################################################################################
# STATIC FILES AND MEDIA
########################################################################################################################

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = f'{SITE_URL}/static/'
STATIC_ROOT = '/var/www/html/static/'

MEDIA_URL = f'{SITE_URL}/media/'
MEDIA_ROOT = '/var/www/html/media/'
TEMPORARY_MEDIA = '{}temp'.format(MEDIA_ROOT)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

########################################################################################################################
# CORS
########################################################################################################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

# CORS_ORIGIN_ALLOW_ALL = False
#
# CORS_ORIGIN_WHITELIST = (
#     'http//:localhost:8000',
# )


########################################################################################################################
# Celery
########################################################################################################################

CELERY_BROKER = 'pyamqp://guest@localhost//'
BROKER_URL = 'pyamqp://guest@localhost//'

########################################################################################################################
# Channels
########################################################################################################################
ASGI_APPLICATION = "loan_management.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            "symmetric_encryption_keys": [SECRET_KEY]
        },
    },
}

########################################################################################################################
# Paypal
########################################################################################################################
PAYPAL_IDENTITY_TOKEN = "AQfY1KxzrVB9QHJFDG2_Nc21EJwkp616_zGvj6lhfgKp5CceOtKUZK_sY7dcsDnncPXPNq08MSAIfsAM"
PAYPAL_RECEIVER_EMAIL = 'sb-x5g7v25723148@business.example.com'
PAYPAL_TEST = True

########################################################################################################################
# EMAIL
########################################################################################################################
# DEFAULT_FROM_EMAIL = 'info@fcusrvotingsystem.com'
SENDGRID_API_KEY = "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"
DEFAULT_FROM_EMAIL = 'info@fcusronlinevoting.com'

########################################################################################################################
# TWILIO
########################################################################################################################
ACCOUNT_SID = 'AC14a8f57bef40cd6614b2089788fa6f53'
AUTH_TOKEN = 'ef7ffa20a2f211d8b267135a6692cc09'
FROM_NUMBER = '+16813217068'