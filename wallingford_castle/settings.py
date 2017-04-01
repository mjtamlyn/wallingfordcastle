import os

from django.core.urlresolvers import reverse_lazy
import dj_database_url
import stripe


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
    'membership',
    'beginners',

    'custom_user',
    'django_object_actions',
    'floppyforms',

    'debug_toolbar',

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'wallingford_castle.urls'
WSGI_APPLICATION = 'wallingford_castle.wsgi.application'

DATABASES = {'default': dj_database_url.config(default='postgresql://localhost/wallingford_castle')}

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    MIDDLEWARE_CLASSES = ('sslify.middleware.SSLifyMiddleware',) + MIDDLEWARE_CLASSES

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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
    EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
    EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'

AUTH_USER_MODEL = 'wallingford_castle.User'
LOGIN_REDIRECT_URL = reverse_lazy('membership:overview')
PASSWORD_RESET_TIMEOUT_DAYS = 14  # Also used for welcome email

SOURCE_VERSION = os.environ.get('SOURCE_VERSION', 'dev')

GA_TRACKING = os.environ.get('GA_TRACKING', '')

SLACK_MEMBERSHIP_HREF = os.environ.get('SLACK_MEMBERSHIP_HREF', '')
SLACK_BEGINNERS_HREF = os.environ.get('SLACK_BEGINNERS_HREF', '')

STRIPE_KEY = os.environ.get('STRIPE_KEY', 'pk_test_Y1b88Dl9MMyGcRJQLnyHyOVI')
stripe.api_key = STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
