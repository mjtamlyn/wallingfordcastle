import datetime

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from venues.tests.factories import VenueFactory
from wallingford_castle.tests.factories import ArcherFactory

from ..lanes import Slot, Template
from .factories import BookedSlotFactory, BookingTemplateFactory


class TestFactoriesAndStr(TestCase):
    def test_booked_slot(self):
        booked_slot = BookedSlotFactory.create()
        str(booked_slot)

    def test_booked_slot_factory_with_archers(self):
        archer = ArcherFactory.create()
        BookedSlotFactory.create(archers=[archer])

    def test_booking_factory(self):
        booking_template = BookingTemplateFactory.create()
        str(booking_template)


class TestBookedSlot(TestCase):
    def test_as_slot(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booked = BookedSlotFactory.build(start=now, duration=hour, target=1)
        slot = Slot(start=now, duration=hour, venue=booked.venue.slug, target=1, booked=True, group_name='')
        self.assertEqual(booked.slot, slot)

    def test_can_serialize_without_venue(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booked = BookedSlotFactory.build(start=now, duration=hour, target=1, venue=None)
        self.assertEqual(booked.slot.venue, None)


class TestBookingTemplate(TestCase):
    def test_simple_template(self):
        now = timezone.now()
        midday = now.replace(hour=12, minute=0, second=0, microsecond=0)
        midday = midday.astimezone(settings.TZ)
        today = midday.date()
        midday_time = midday.time()
        hour = datetime.timedelta(hours=1)

        booking_template = BookingTemplateFactory.build(
            date=today,
            start_times=[midday_time],
            targets=3,
            booking_duration=hour,
        )
        template = Template(
            start_times=[midday],
            targets=3,
            slot_duration=hour,
            venue=booking_template.venue.slug,
        )
        self.assertEqual(booking_template.template, template)

    def test_has_bookings(self):
        now = timezone.now()
        midday = now.replace(hour=12, minute=0, second=0, microsecond=0)
        midday = midday.astimezone(settings.TZ)
        today = midday.date()
        midday_time = midday.time()
        hour = datetime.timedelta(hours=1)

        venue = VenueFactory.create()

        booked_slot = BookedSlotFactory.create(venue=venue, start=midday, duration=hour, target=1)

        booking_template = BookingTemplateFactory.build(
            venue=venue,
            date=today,
            start_times=[midday_time],
            targets=3,
            booking_duration=hour,
        )
        template = Template(
            start_times=[midday],
            venue=venue.slug,
            targets=3,
            slot_duration=hour,
            booked_slots=[booked_slot.slot],
        )
        self.assertEqual(booking_template.template, template)

    def test_create_next_simple(self):
        template = BookingTemplateFactory.create()
        new = template.create_next()
        self.assertEqual(template.title, new.title)
        self.assertEqual(template.date + datetime.timedelta(days=7), new.date)
        self.assertEqual(template.notes, new.notes)
        self.assertEqual(template.start_times, new.start_times)
        self.assertEqual(template.targets, new.targets)
        self.assertEqual(template.booking_duration, new.booking_duration)
        self.assertEqual(template.multiple_archers_permitted, new.multiple_archers_permitted)
        self.assertEqual(template.distance_required, new.distance_required)

    def test_create_next_specified_date(self):
        template = BookingTemplateFactory.create()
        date = datetime.date(2040, 1, 1)
        new = template.create_next(date=date)
        self.assertEqual(new.date, date)
