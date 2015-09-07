import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', 'not-a-secret')

DEBUG = not (os.environ.get('DEBUG', '') == 'False')

ALLOWED_HOSTS = [
    'wallingfordcastle.herokuapp.com',
    'wallingfordcastle.co.uk',
    'www.wallingfordcastle.co.uk',
]

INSTALLED_APPS = (
    'wallingford_castle',

    'floppyforms',

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
    'django.middleware.security.SecurityMiddleware',
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

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'wallingford_castle.context_processors.ga',
            'wallingford_castle.context_processors.source_version',
        )
    }
}]

SOURCE_VERSION = os.environ.get('SOURCE_VERSION', 'dev')

GA_TRACKING = os.environ.get('GA_TRACKING', '')

SLACK_MEMBERSHIP_HREF = os.environ.get('SLACK_MEMBERSHIP_HREF', '')
SLACK_BEGINNERS_HREF = os.environ.get('SLACK_MEMBERSHIP_HREF', '')
