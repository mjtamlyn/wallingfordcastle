from django.conf import settings


def ga(request):
    if settings.GA_TRACKING:
        return {'GA_TRACKING': settings.GA_TRACKING}
    return {}
