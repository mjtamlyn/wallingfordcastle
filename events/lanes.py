import copy
from collections import defaultdict

import attr

from django.utils.functional import cached_property


@attr.s
class Slot:
    start = attr.ib()
    duration = attr.ib()
    target = attr.ib()
    booked = attr.ib(default=False)
    details = attr.ib(default=None, cmp=False)

    @property
    def end(self):
        return self.start + self.duration

    def overlaps(self, other):
        if self.end <= other.start:
            return False
        if self.start >= other.end:
            return False
        return True

    def serialize(self):
        details = None
        if self.details:
            details = ', '.join(self.details.archers.values_list('name', flat=True))
            print(details)
        return {
            '__type': 'Slot',
            'start': self.start.strftime('%Y-%m-%dT%H:%M'),
            'end': self.end.strftime('%Y-%m-%dT%H:%M'),
            'duration': self.duration.seconds // 60,
            'target': self.target,
            'booked': self.booked,
            'details': details,
        }


@attr.s
class Template:
    start_times = attr.ib()
    targets = attr.ib()
    slot_duration = attr.ib()
    booked_slots = attr.ib(default=attr.Factory(list))

    @cached_property
    def slots(self):
        schedule = []
        start_times = copy.copy(self.start_times)

        exact_lookup = {}
        target_lookup = defaultdict(list)
        for booking in self.booked_slots:
            if booking.start not in start_times:
                start_times.append(booking.start)
            exact_lookup[(booking.start, booking.target)] = booking
            target_lookup[booking.target].append(booking)
        start_times.sort()

        for start_time in start_times:
            slots = []
            for i in range(1, self.targets + 1):
                booked = exact_lookup.get((start_time, i))
                if booked:
                    slots.append(booked)
                elif start_time in self.start_times:
                    slot = Slot(
                        start=start_time,
                        duration=self.slot_duration,
                        target=i,
                    )
                    if any(slot.overlaps(booking) for booking in target_lookup[i]):
                        slot = None
                    slots.append(slot)
                else:
                    slots.append(None)
            schedule.append({
                'start_time': start_time,
                'slots': slots,
            })
        return schedule

    def serialize(self):
        return [{
            'startTime': row['start_time'].strftime('%Y-%m-%dT%H:%M'),
            'slots': [slot.serialize() if slot else None for slot in row['slots']],
        } for row in self.slots]
