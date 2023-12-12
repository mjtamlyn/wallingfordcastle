import os
import zoneinfo

from django.urls import reverse_lazy

import dj_database_url
import sentry_sdk
import stripe
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', 'not-a-secret')

DEBUG = not (os.environ.get('DEBUG', '') == 'False')

ALLOWED_HOSTS = [
    'wallingfordcastle.herokuapp.com',
    'wallingfordcastle.co.uk',
    'www.wallingfordcastle.co.uk',
]
if DEBUG:
    ALLOWED_HOSTS += ['localhost']

INSTALLED_APPS = (
    'wallingford_castle',
    'archery',
    'membership',
    'beginners',
    'bookings',
    'coaching',
    'courses',
    'events',
    'payments',
    'records',
    'tournaments',
    'venues',

    'custom_user',
    'django_object_actions',

    'debug_toolbar',
    'webpack_loader',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wallingford_castle.middleware.TimezoneMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'wallingford_castle.urls'
WSGI_APPLICATION = 'wallingford_castle.wsgi.application'

DATABASES = {'default': dj_database_url.config(default='postgresql://localhost/wallingford_castle')}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
TZ = zoneinfo.ZoneInfo(TIME_ZONE)
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'build')]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'build', 'webpack-stats.json'),
    },
}

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

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
            'django.template.context_processors.request',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'wallingford_castle.context_processors.ga',
            'wallingford_castle.context_processors.source_version',
        )
    }
}]

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

AUTH_USER_MODEL = 'wallingford_castle.User'
LOGIN_REDIRECT_URL = reverse_lazy('membership:overview')
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365  # Expire sessions only once a year
PASSWORD_RESET_TIMEOUT_DAYS = 14  # Also used for welcome email

SOURCE_VERSION = os.environ.get('SOURCE_VERSION', 'dev')

if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn="https://2e73dabd986c446fb77471128a59d91c@sentry.io/1285738",
        release=SOURCE_VERSION,
        integrations=[DjangoIntegration()]
    )

GA_TRACKING = os.environ.get('GA_TRACKING', '')

SLACK_MEMBERSHIP_HREF = os.environ.get('SLACK_MEMBERSHIP_HREF', '')
SLACK_BEGINNERS_HREF = os.environ.get('SLACK_BEGINNERS_HREF', '')
SLACK_TOURNAMENT_HREF = os.environ.get('SLACK_TOURNAMENT_HREF', '')
SLACK_EVENTS_HREF = os.environ.get('SLACK_EVENTS_HREF', '')
SLACK_COACHING_HREF = os.environ.get('SLACK_COACHING_HREF', '')

STRIPE_KEY = os.environ.get('STRIPE_KEY', 'pk_test_Y1b88Dl9MMyGcRJQLnyHyOVI')
stripe.api_key = STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

STRIPE_PRICES = {
    'adult': {
        'id': os.environ.get('STRIPE_PRICES_ADULT', 'price_1HXOx7BZ7K43BUB4SACbBRqW'),
        'price': 20,
    },
    'concession': {
        'id': os.environ.get('STRIPE_PRICES_CONCESSION', 'price_1HXOxRBZ7K43BUB43bdWQErn'),
        'price': 15,
    },
    'non-shooting': {
        'id': os.environ.get('STRIPE_PRICES_NON_SHOOTING', 'non-shooting'),
        'price': 5,
    },
    'coaching-adult': {
        'id': os.environ.get('STRIPE_PRICES_COACHING_ADULT', 'price_1HXOyBBZ7K43BUB4cIRekPDI'),
        'price': 30,
    },
    'coaching-junior': {
        'id': os.environ.get('STRIPE_PRICES_COACHING_JUNIOR', 'price_1NvbycBZ7K43BUB4INdqPR01'),
        'price': 25,
    },
    'coaching-junior-conversion': {
        'id': os.environ.get('STRIPE_PRICES_COACHING_JUNIOR_CONVERSION', 'price_1NvbyqBZ7K43BUB4vlvdTRy1'),
        'price': 50,
    },
    'coaching-junior-performance': {
        'id': os.environ.get('STRIPE_PRICES_COACHING_JUNIOR_PERFORMANCE', 'price_1Nvbz1BZ7K43BUB4eFaea1MF'),
        'price': 90,
    },
    'coaching-gym': {
        'id': os.environ.get('STRIPE_PRICES_COACHING_GYM', 'price_1NvbzSBZ7K43BUB4TApNmQSz'),
        'price': 15,
    },
}
