import datetime

from django.utils import timezone

import factory
import factory.django
import factory.fuzzy

from venues.tests.factories import VenueFactory

from ..models import BookedSlot, BookingTemplate


class BookedSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookedSlot

    start = factory.fuzzy.FuzzyDateTime(
        timezone.now() - datetime.timedelta(days=7),
        timezone.now() + datetime.timedelta(days=7),
    )
    duration = datetime.timedelta(hours=1)
    target = 1
    venue = factory.SubFactory(VenueFactory)

    @factory.post_generation
    def archers(obj, create, extracted, **kwargs):
        if not create or not extracted:
            return
        obj.archers.set(extracted)


class BookingTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookingTemplate

    venue = factory.SubFactory(VenueFactory)
    date = factory.fuzzy.FuzzyDateTime(
        timezone.now() - datetime.timedelta(days=7),
        timezone.now() + datetime.timedelta(days=7),
    )
    start_times = [datetime.time(12, 0, 0)]
    targets = 3
    booking_duration = datetime.timedelta(hours=1)
