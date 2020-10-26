import datetime

from django.test import TestCase
from django.utils import timezone

import pytz

from ..lanes import Slot, Template
from ..models import BookedSlot, BookingTemplate


class TestBookedSlot(TestCase):
    def test_as_slot(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booked = BookedSlot(start=now, duration=hour, target=1)
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
        
        booking_template = BookingTemplate(
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

        booked_slot = BookedSlot.objects.create(start=midday, duration=hour, target=1)
        
        booking_template = BookingTemplate(
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
