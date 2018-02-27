from django.views.generic import ListView
from django.utils import timezone

from .models import Event


class EventList(ListView):
    model = Event
    template_name = 'events/bookable_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        bookable_events = Event.objects.filter(bookable=True).order_by('date')
        return bookable_events.filter(date__gt=timezone.now())
