import datetime

from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models
from django.utils.functional import cached_property

import pytz

from wallingford_castle.models import Archer

from .lanes import Slot, Template


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    date = models.DateTimeField()
    duration = models.DurationField()
    bookable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def start(self):
        return self.date

    @property
    def end(self):
        return self.date + self.duration

    def attendee_count(self):
        return self.attendee_set.count()


class Attendee(models.Model):
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE, related_name='event_attendance_set')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return 'Archer %s attending event %s' % (self.archer_id, self.event_id)

    class Meta:
        unique_together = ['archer', 'event']


class BookingQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['event', 'order']


class Booking(models.Model):
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response_answers = HStoreField()

    def __str__(self):
        return 'Archer %s booking in for event %s' % (self.archer_id, self.event_id)

    class Meta:
        unique_together = ['archer', 'event']

    @property
    def responses(self):
        return '\n'.join(['%s - %s' % (question, answer) for question, answer in self.response_answers.items()])

    def answers(self):
        questions = self.event.bookingquestion_set.order_by('order')
        for q in questions:
            yield self.response_answers.get(q.text, '')


class BookedSlot(models.Model):
    start = models.DateTimeField()
    duration = models.DurationField()
    target = models.PositiveIntegerField()
    distance = models.CharField(max_length=100, default='', blank=True)
    archers = models.ManyToManyField(Archer)

    # Group fields
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=100, default='', blank=True)
    number_of_targets = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('start', 'target')

    def __str__(self):
        return 'Slot booked on target %s at %s' % (self.target, self.start)

    @property
    def end(self):
        return self.start + self.duration

    @cached_property
    def slot(self):
        return Slot(
            start=self.start,
            duration=self.duration,
            target=self.target,
            number_of_targets=self.number_of_targets,
            booked=True,
            details=self,
            is_group=self.is_group,
            group_name=self.group_name,
        )


class BookingTemplate(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    start_times = ArrayField(models.TimeField())
    targets = models.PositiveIntegerField()
    booking_duration = models.DurationField()
    multiple_archers_permitted = models.BooleanField(default=True)
    distance_required = models.BooleanField(default=True)

    def __str__(self):
        return 'Booking template for %s' % self.date

    @cached_property
    def template(self):
        tz = pytz.timezone('Europe/London')
        slots = [slot.slot for slot in self.slots]
        start_times = [
            tz.localize(datetime.datetime.combine(self.date, time))
            for time in self.start_times
        ]
        return Template(
            start_times=start_times,
            targets=self.targets,
            slot_duration=self.booking_duration,
            booked_slots=slots,
        )

    @property
    def slots(self):
        tz = pytz.timezone('Europe/London')
        midnight = datetime.datetime.combine(self.date, datetime.time(0))
        midnight = tz.localize(midnight)
        return BookedSlot.objects.filter(
            start__gte=midnight,
            start__lt=midnight + datetime.timedelta(days=1),
        )

    def create_next(self, date=None):
        tz = pytz.timezone('Europe/London')

        if date is None:
            date = self.date + datetime.timedelta(days=7)
        new = BookingTemplate.objects.create(
            date=date,
            title=self.title,
            notes=self.notes,
            start_times=self.start_times,
            targets=self.targets,
            booking_duration=self.booking_duration,
            multiple_archers_permitted=self.multiple_archers_permitted,
            distance_required=self.distance_required,
        )
        slots = self.slots.filter(is_group=True)
        for slot in slots:
            start_time = datetime.datetime.combine(new.date, slot.start.time())
            start_time = tz.localize(start_time)
            new_slot = BookedSlot.objects.create(
                start=start_time,
                duration=slot.duration,
                target=slot.target,
                distance=slot.distance,
                is_group=slot.is_group,
                group_name=slot.group_name,
                number_of_targets=slot.number_of_targets,
            )
            new_slot.archers.set(slot.archers.all())
        return new
