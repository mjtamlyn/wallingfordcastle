import datetime

from django.http import Http404, JsonResponse
from django.utils import timezone

from .models import BookingTemplate


def date_list(request):
    today = timezone.now().date()
    prebooking_limit = today + datetime.timedelta(days=7)

    if request.user.is_superuser:
        templates = BookingTemplate.objects.order_by('date')
    else:
        templates = BookingTemplate.objects.order_by('date').filter(date__lte=prebooking_limit)
    response = {
        'dates': [{
            '__type': 'BookableDate',
            'api': template.date.strftime('%Y-%m-%d'),
            'pretty': template.date.strftime('%A %-d %B'),
        } for template in templates]
    }
    return JsonResponse(response)


def date_slots(request, date):
    today = timezone.now().date()
    prebooking_limit = today + datetime.timedelta(days=7)

    if request.user.is_superuser:
        templates = BookingTemplate.objects
    else:
        templates = BookingTemplate.objects.filter(date__lte=prebooking_limit)

    try:
        template = templates.get(date=datetime.datetime.strptime(date, '%Y-%m-%d').date())
    except BookingTemplate.DoesNotExist:
        raise Http404('No bookings for that date')

    response = {
        'date': {
            '__type': 'BookableDate',
            'api': template.date.strftime('%Y-%m-%d'),
            'pretty': template.date.strftime('%A %-d %B'),
        },
        'schedule': template.template.serialize(),
    }
    return JsonResponse(response)
