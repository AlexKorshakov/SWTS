"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from .. import apps

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent  # BASE_DIR = \\application\\config\\web

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w4tg(gh+92o1a@@6=vri+zkj&^drxq^#b+vp5&k-%sn*cdxye+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Register installed apps
    *[app.Config.name for app in apps.INSTALLED_APPS],
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.web.middlewares.InjectMiddleware",
]

ROOT_URLCONF = "config.web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR.parent.parent, 'apps\\core\\web\\templates')  # BASE_DIR = \\application\\config\\web
        ],

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

WSGI_APPLICATION = "config.web.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent.parent / 'HSEViolationsDataBase.db',
    }
}  # BASE_DIR = \\application\\config\\web

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
     },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
     },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
     },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"
ZERO = timedelta(0)

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# BASE_DIR = \\application\\config\\web
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# BASE_DIR = \\application\\config\\web
MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, 'media')
MEDIA_URL = '/media/'

INTERNAL_IPS = [
    "127.0.0.1",
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR.parent, 'django_cache'),
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 100
        }
    }
}
# LOGGING_LEVEL = 'DEBUG'
LOGGING_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "rich": {
            "datefmt": "[%X]"
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'rich.logging.RichHandler',
            'formatter': 'rich'
        },
        'file': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': f'{BASE_DIR.parent}/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': LOGGING_LEVEL,
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'django.request': {
            'level': LOGGING_LEVEL,
            'handlers': ['console', 'file'],
            'propagate': True
        }
    }

}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
if __name__ == '__main__':
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent  # BASE_DIR = \\application\\config\\web
    print(f'{BASE_DIR =}')
    print(f'{BASE_DIR.parent =}')
    print(f'{BASE_DIR.parent.parent =}')
