import datetime

from django.test import TestCase
from django.utils import timezone

import pytz

from wallingford_castle.tests.factories import ArcherFactory

from ..lanes import Slot, Template
from ..models import BookedSlot
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
        slot = Slot(start=now, duration=hour, target=1, booked=True, group_name='')
        self.assertEqual(booked.slot, slot)


class TestBookingTemplate(TestCase):
    def test_simple_template(self):
        now = timezone.now()
        tz = pytz.timezone('Europe/London')
        midday = now.replace(hour=12, minute=0, second=0, microsecond=0)
        midday = midday.astimezone(tz)
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
            slot_duration=hour
        )
        self.assertEqual(booking_template.template, template)

    def test_has_bookings(self):
        now = timezone.now()
        tz = pytz.timezone('Europe/London')
        midday = now.replace(hour=12, minute=0, second=0, microsecond=0)
        midday = midday.astimezone(tz)
        today = midday.date()
        midday_time = midday.time()
        hour = datetime.timedelta(hours=1)

        booked_slot = BookedSlotFactory.create(start=midday, duration=hour, target=1)

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

    def test_create_next_copies_group_slots(self):
        archer_1 = ArcherFactory.create()
        archer_2 = ArcherFactory.create()

        template = BookingTemplateFactory.create(targets=2)
        tz = pytz.timezone('Europe/London')
        start_time = datetime.datetime.combine(template.date, template.start_times[0])
        start_time = start_time.astimezone(tz)
        booked_group = BookedSlotFactory.create(
            start=start_time,
            target=1,
            is_group=True,
            archers=[archer_1],
        )
        BookedSlotFactory.create(
            start=start_time,
            target=2,
            is_group=False,
            archers=[archer_2],
        )

        template.create_next()
        # TODO: fix timezones! This won't work in summer time.
        # next_start_time = start_time + datetime.timedelta(days=7)
        # new_slots = new.slots.filter(start=next_start_time)
        # self.assertEqual(new_slots.count(), 1)
        new_slot = BookedSlot.objects.order_by('-id').first()
        self.assertTrue(new_slot.is_group)
        self.assertEqual(new_slot.target, booked_group.target)
        self.assertSequenceEqual(new_slot.archers.all(), [archer_1])
