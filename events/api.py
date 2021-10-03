import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils import timezone

from membership.models import Member

from .forms import BookSlotForm, CancelSlotForm
from .models import BookingTemplate


@login_required
def date_list(request):
    today = timezone.now().date()
    prebooking_limit = today + datetime.timedelta(days=7)

    templates = BookingTemplate.objects.order_by('date').select_related('venue').filter(date__gte=today)
    if not request.user.is_superuser:
        templates = templates.filter(date__lte=prebooking_limit)
    response = {
        'dates': [{
            '__type': 'BookableDate',
            'api': template.date.strftime('%Y-%m-%d'),
            'pretty': template.date.strftime('%A %-d %B'),
            'title': template.title or None,
            'notes': template.notes or None,
        } for template in templates]
    }
    return JsonResponse(response)


@login_required
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

    venue = None
    if template.venue:
        venue = {
            'name': template.venue.name,
            'link': reverse('venues:detail', kwargs={'slug': template.venue.slug}),
        }

    response = {
        'date': {
            '__type': 'BookableDate',
            'api': template.date.strftime('%Y-%m-%d'),
            'pretty': template.date.strftime('%A %-d %B'),
            'title': template.title or None,
            'notes': template.notes or None,
        },
        'venue': venue,
        'schedule': template.template.serialize(user=request.user),
        'options': {
            'distanceRequired': template.distance_required,
            'multipleArchersPermitted': template.multiple_archers_permitted,
            'abFaces': template.ab_faces,
        },
    }
    return JsonResponse(response)


@login_required
def bookable_archers(request):
    members = Member.objects.managed_by(request.user)
    response = {
        'archers': [{
            '__type': 'Archer',
            'name': member.archer.name,
            'id': member.id,
        } for member in members],
    }
    return JsonResponse(response)


@login_required
def book_slot(request):
    ok = False
    data = json.loads(request.body)
    form = BookSlotForm(data=data, user=request.user)
    if form.is_valid():
        form.save()
        ok = True
    # TODO: some sort of helpful error cases!
    response = {
        'ok': ok,
    }
    return JsonResponse(response)


@login_required
def cancel_slot(request):
    ok = False
    data = json.loads(request.body)
    form = CancelSlotForm(data=data, user=request.user)
    if form.is_valid():
        form.save()
        ok = True
    # TODO: some sort of helpful error cases!
    response = {
        'ok': ok,
    }
    return JsonResponse(response)
