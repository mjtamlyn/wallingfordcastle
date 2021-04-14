import copy
from collections import defaultdict

from django.conf import settings
from django.utils.functional import cached_property

import attr


def serialize_time(time):
    local = time.astimezone(settings.TZ)
    return local.strftime('%Y-%m-%dT%H:%M')


@attr.s
class Slot:
    start = attr.ib()
    duration = attr.ib()
    target = attr.ib()
    number_of_targets = attr.ib(default=1)
    booked = attr.ib(default=False)
    details = attr.ib(default=None, cmp=False)

    is_group = attr.ib(default=False)
    group_name = attr.ib(default=None)

    @property
    def end(self):
        return self.start + self.duration

    def overlaps(self, other):
        if self.end <= other.start:
            return False
        if self.start >= other.end:
            return False
        return True

    def personalize(self, user):
        self.editable = False
        if user is None or self.is_group:
            return self
        if user.manages_any(self.booked_archers):
            self.editable = True
        return self

    @cached_property
    def booked_archers(self):
        if self.details is None:
            return []
        return list(self.details.archers.order_by('name'))

    def serialize(self):
        details = None
        if self.details:
            names = ', '.join(a.name for a in self.booked_archers)
            details = {
                'names': names,
                'distance': self.details.distance,
            }
        return {
            '__type': 'Slot',
            'start': serialize_time(self.start),
            'end': serialize_time(self.end),
            'duration': self.duration.seconds // 60,
            'target': self.target,
            'numberOfTargets': self.number_of_targets,
            'booked': self.booked,
            'details': details,
            'groupName': self.group_name,
            'editable': self.editable,
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
            start = booking.start.astimezone(settings.TZ)
            if start not in start_times:
                start_times.append(start)
            exact_lookup[(start, booking.target)] = booking
            for i in range(booking.number_of_targets):
                target_lookup[booking.target + i].append(booking)
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

    def serialize(self, user=None):
        return [{
            'startTime': serialize_time(row['start_time']),
            'endTime': serialize_time(row['start_time'] + self.slot_duration),
            'slots': [slot.personalize(user=user).serialize() if slot else None for slot in row['slots']],
        } for row in self.slots]
