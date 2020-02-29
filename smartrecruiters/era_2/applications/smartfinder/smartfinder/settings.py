import dj_database_url
"""
smartfinder.settings
~~~~~~~~~~~~~~

This module implements high-level Django settings for SmartFinder.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJ_SECRET_KEY', '^a3t)1ri$d*6fs2+)lgcwq7neu=_0wl8=j3ccd6h9=aj)0bxig')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJ_DEBUG_STATE', True)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'sr-smartfinder.herokuapp.com',
    'finder.smartian.space'
]


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project apps
    'app.apps.AppConfig',
    'api.apps.ApiConfig',

    # dependency apps
    'django_cron',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartfinder.urls'

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

WSGI_APPLICATION = 'smartfinder.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartfinder',
        'USER': 'postgres',
        'PASSWORD': 'development'
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Login redirects

LOGIN_REDIRECT_URL = '/accounts/'
LOGOUT_REDIRECT_URL = '/'


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = "/static/"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email settings (Gmail SMTP)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('DJ_EMAIL_HOST', 'localhost')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('DJ_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('DJ_EMAIL_PASSWORD', '')


# Recurring jobs

DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 1
CRON_CLASSES = [
    'api.jobs.Sync',
    'api.jobs.GetAccounts',
    'api.jobs.GetContacts',
    'api.jobs.QualifyContacts',
]
