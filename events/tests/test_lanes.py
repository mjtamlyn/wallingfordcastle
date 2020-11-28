import datetime

from django.test import TestCase
from django.utils import timezone

from ..lanes import Slot, Template


class TestSlot(TestCase):
    def test_slot_basics(self):
        now = timezone.now()
        slot = Slot(
            start=now,
            duration=datetime.timedelta(minutes=90),
            target=1,
        )
        self.assertEqual(slot.end, now + datetime.timedelta(hours=1, minutes=30))

    def test_overalps(self):
        midday = datetime.datetime(2000, 1, 1, 12, 0, 0)
        one = midday + datetime.timedelta(hours=1)
        twelve_one = Slot(
            start=midday,
            duration=datetime.timedelta(minutes=60),
            target=1,
        )
        one_two = Slot(
            start=one,
            duration=datetime.timedelta(minutes=60),
            target=1,
        )
        midday_half_one = Slot(
            start=midday,
            duration=datetime.timedelta(minutes=90),
            target=1,
        )
        self.assertFalse(twelve_one.overlaps(one_two))
        self.assertTrue(twelve_one.overlaps(midday_half_one))
        self.assertTrue(one_two.overlaps(midday_half_one))


class TestTemplate(TestCase):
    maxDiff = 2000

    def test_simple_booked_slots(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        template = Template(
            start_times=[now],
            targets=3,
            slot_duration=hour,
        )
        self.assertEqual(template.slots, [{
            'start_time': now,
            'slots': [
                Slot(start=now, duration=hour, target=1),
                Slot(start=now, duration=hour, target=2),
                Slot(start=now, duration=hour, target=3),
            ],
        }])

    def test_booked_standard_slot(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booking = Slot(start=now, duration=hour, target=2, booked=True)
        template = Template(
            start_times=[now],
            targets=3,
            slot_duration=hour,
            booked_slots=[booking],
        )
        self.assertEqual(template.slots, [{
            'start_time': now,
            'slots': [
                Slot(start=now, duration=hour, target=1),
                booking,
                Slot(start=now, duration=hour, target=3),
            ],
        }])

    def test_booked_double_slot(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booking = Slot(start=now, duration=hour * 2, target=3, booked=True)
        template = Template(
            start_times=[now, now + hour],
            targets=3,
            slot_duration=hour,
            booked_slots=[booking],
        )
        self.assertEqual(template.slots, [{
            'start_time': now,
            'slots': [
                Slot(start=now, duration=hour, target=1),
                Slot(start=now, duration=hour, target=2),
                booking,
            ],
        }, {
            'start_time': now + hour,
            'slots': [
                Slot(start=now + hour, duration=hour, target=1),
                Slot(start=now + hour, duration=hour, target=2),
                None,
            ],
        }])

    def test_booked_weird_slot(self):
        now = timezone.now()
        hour = datetime.timedelta(hours=1)
        booking = Slot(
            start=now + datetime.timedelta(minutes=75),
            duration=hour,
            target=1,
            booked=True,
        )
        template = Template(
            start_times=[now, now + hour],
            targets=3,
            slot_duration=hour,
            booked_slots=[booking],
        )
        self.assertEqual(template.slots, [{
            'start_time': now,
            'slots': [
                Slot(start=now, duration=hour, target=1),
                Slot(start=now, duration=hour, target=2),
                Slot(start=now, duration=hour, target=3),
            ],
        }, {
            'start_time': now + hour,
            'slots': [
                None,
                Slot(start=now + hour, duration=hour, target=2),
                Slot(start=now + hour, duration=hour, target=3),
            ],
        }, {
            'start_time': booking.start,
            'slots': [
                booking,
                None,
                None,
            ],
        }])
