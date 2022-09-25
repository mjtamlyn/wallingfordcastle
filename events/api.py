import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils import timezone

from membership.models import Member

from .forms import BookSlotForm, CancelSlotForm
from .models import BookedSlot, BookingTemplate


@login_required
def date_list(request):
    today = timezone.now().date()
    prebooking_limit = today + datetime.timedelta(days=7)

    templates = BookingTemplate.objects.order_by('date').select_related('venue').filter(date__gte=today)
    if not request.user.is_superuser:
        templates = templates.filter(date__lte=prebooking_limit)
    templates = templates.distinct('date')
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

    templates = templates.filter(date=date).order_by('venue_id')
    if not templates:
        raise Http404('No bookings for that date')

    response = {'venues': []}
    for template in templates:
        venue = None
        if template.venue:
            venue = {
                'name': template.venue.name,
                'key': template.venue.slug,
                'link': reverse('venues:detail', kwargs={'slug': template.venue.slug}),
            }

        response['venues'].append({
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
                'bRange': bool(template.b_targets),
            },
        })
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
    data = json.loads(request.body)
    form = BookSlotForm(data=data, user=request.user)
    if form.is_valid():
        form.save()
        response = {'ok': True}
    else:
        response = {
            'ok': False,
            'errors': form.errors.get_json_data(),
        }
    return JsonResponse(response)


@login_required
def cancel_slot(request):
    data = json.loads(request.body)
    form = CancelSlotForm(data=data, user=request.user)
    if form.is_valid():
        form.save()
        response = {'ok': True}
    else:
        response = {
            'ok': False,
            'errors': form.errors.get_json_data(),
        }
    return JsonResponse(response)


@login_required
def slot_absentable_archers(request, slot):
    members = Member.objects.managed_by(request.user)
    try:
        slot = BookedSlot.objects.get(**slot)
    except BookedSlot.DoesNotExist:
        raise Http404('Could not find a booked slot at that time')
    archers = sorted(set(member.archer for member in members) & set(slot.archers.all()), key=lambda a: a.name)
    response = {
        'archers': [{
            '__type': 'Archer',
            'name': archer.name,
            'id': archer.id,
        } for archer in archers],
    }
    return JsonResponse(response)
