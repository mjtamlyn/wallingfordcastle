import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', 'not-a-secret')

DEBUG = not (os.environ.get('DEBUG', '') == 'False')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'wallingfordcastle.herokuapp.com',
    'wallingfordcastle.co.uk',
    'www.wallingfordcastle.co.uk',
]

INSTALLED_APPS = (
    'wallingford_castle',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wallingford_castle.urls'
WSGI_APPLICATION = 'wallingford_castle.wsgi.application'

DATABASES = {'default': dj_database_url.config(default='postgresql://localhost/wallingford_castle')}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
