import json

from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, ListView
from django.views.generic.detail import SingleObjectMixin

import requests

from wallingford_castle.mixins import FullMemberRequired

from .forms import BookEventForm
from .models import Event


class EventList(FullMemberRequired, ListView):
    model = Event
    template_name = 'events/bookable_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        bookable_events = Event.objects.filter(bookable=True, date__gt=timezone.now()).order_by('date')
        user = self.request.user
        for event in bookable_events:
            event.registered_members = event.booking_set.filter(Q(archer__user=user) | Q(archer__managing_users=user))
        return bookable_events


class BookEvent(FullMemberRequired, SingleObjectMixin, FormView):
    model = Event
    template_name = 'events/book_event.html'
    context_object_name = 'event'
    form_class = BookEventForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        bookable_events = Event.objects.filter(bookable=True).order_by('date')
        return bookable_events.filter(date__gt=timezone.now())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'event': self.object,
            'user': self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        booking = form.save()
        if settings.SLACK_EVENTS_HREF:
            data = json.dumps({
                'icon_emoji': ':white_check_mark:',
                'text': '%s has registered for %s!' % (
                    booking.archer,
                    booking.event,
                )
            })
            try:
                requests.post(settings.SLACK_EVENTS_HREF, data=data)
            except Exception:
                pass
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('events:event-list')
