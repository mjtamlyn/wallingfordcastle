import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallingford_castle.settings")


from django.core.wsgi import get_wsgi_application  # NOQA

application = get_wsgi_application()
