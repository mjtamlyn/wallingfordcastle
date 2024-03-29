import json

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import ArcherSeason, Event, Registration


def plan_info(request, plan_id):
    plan = get_object_or_404(ArcherSeason, pk=plan_id)
    archer = plan.archer
    if (
            archer.user_id != request.user.pk and request.user not in archer.managing_users.all() and
            not request.user.is_superuser
    ):
        raise Http404
    response = {
        'archer': str(plan.archer),
        'ageGroup': plan.archer.age_group,
        'season': str(plan.season),
        'targetClassification': {
            'id': plan.target_classification,
            'name': plan.get_target_classification_display(),
        },
        'personalisedTargetComments': plan.personalised_target_comments,
    }

    tracks = plan.season.competitivetrack_set.order_by('number')
    track_data = []
    for track in tracks:
        archer_track = plan.archertrack_set.filter(track=track).first()
        track_data.append({
            'tier': track.number,
            'tierName': 'Tier %s' % track.number,
            'name': track.name,
            'comments': archer_track.recommended_events_comments if archer_track else None,
        })
        events = track.event_set.order_by('date').select_related('tournament', 'event')
        event_data = []
        for event in events:
            registration = plan.registration_set.filter(event=event).first()
            event = {
                'name': event.name,
                'eventFormat': event.event_format,
                'ageGroups': event.age_groups,
                'scayt': event.scayt,
                'date': {
                    'api': event.date.isoformat(),
                    'pretty': event.date.strftime('%A %-d %B'),
                },
                'endDate': {
                    'api': event.end_date.isoformat(),
                    'pretty': event.end_date.strftime('%A %-d %B'),
                } if event.end_date else None,
                'venue': {
                    'name': event.venue,
                    'postCode': event.venue_post_code,
                },
                'tournament': {
                    'id': event.tournament_id,
                    'link': event.tournament.get_absolute_url(),
                } if event.tournament else None,
                'clubEvent': {
                    'id': event.event_id,
                    'link': reverse('events:book-event', kwargs={'pk': event.event_id}),
                } if event.event else None,
                'clubTrip': event.club_trip,
                'entryLink': event.entry_link,
                'registration': {
                    'status': {
                        'id': registration.status,
                        'display': registration.get_status_display(),
                    },
                    'wantsTransport': {
                        'id': registration.wants_transport,
                        'display': registration.get_wants_transport_display(),
                    },
                } if registration else None,
                'registrationLink': reverse('coaching-api:register', kwargs={
                    'plan_id': plan_id,
                    'event_id': event.pk,
                }),
            }
            event_data.append(event)
        track_data[-1]['events'] = event_data
    response['tracks'] = track_data
    return JsonResponse(response)


def register(request, plan_id, event_id):
    plan = get_object_or_404(ArcherSeason, pk=plan_id)
    event = get_object_or_404(Event, pk=event_id)
    data = json.loads(request.body)
    status = data['status']
    wants_transport = data.get('wantsTransport', None)

    if not status:
        plan.registration_set.filter(event=event).delete()
        return JsonResponse({'ok': True})

    try:
        registration = plan.registration_set.get(event=event)
    except Registration.DoesNotExist:
        plan.registration_set.create(event=event, status=status, wants_transport=wants_transport)
    else:
        registration.status = status
        registration.wants_transport = wants_transport
        registration.save()

    return JsonResponse({'ok': True})
