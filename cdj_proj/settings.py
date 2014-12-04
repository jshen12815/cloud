"""
Django settings for cdj_proj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '91q&ig52##jp-!ato4xp&uoxp81l=943y_=45ke)fu^@7gje&w'

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'cdj_proj.urls'

WSGI_APPLICATION = 'cdj_proj.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/clouddj/login'
LOGIN_REDIRECT_URL = '/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

if not DEBUG:
    import dj_database_url

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['team-clouddj.herokuapp.com']

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    AWS_STORAGE_BUCKET_NAME = 'clouddj'
    AWS_ACCESS_KEY_ID = 'AKIAJ5ELVALE5EFUVQJA'
    AWS_SECRET_ACCESS_KEY = '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'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % 'clouddj'
    STATIC_URL = S3_URL

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'clouddj',
        'widget_tweaks',
        'storages',
        'boto',
    )

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'


    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'clouddj.webapp@gmail.com'
    EMAIL_HOST_PASSWORD = 'alisonistaylorswiftsmiddlename'
    EMAIL_USE_TLS = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/

    STATIC_ROOT = 'staticfiles'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

else:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'clouddj',
        'widget_tweaks',
    )

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'clouddj',
            'USER': 'webapps',
            'PASSWORD': 'fun',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')