import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
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
            booked=True,
            details=self,
        )


class BookingTemplate(models.Model):
    date = models.DateField()
    start_times = ArrayField(models.TimeField())
    targets = models.PositiveIntegerField()
    booking_duration = models.DurationField()

    def __str__(self):
        return 'Booking template for %s' % self.date

    @cached_property
    def template(self):
        tz = pytz.timezone('Europe/London')
        midnight = datetime.datetime.combine(self.date, datetime.time(0))
        midnight = tz.localize(midnight)
        slots = [slot.slot for slot in BookedSlot.objects.filter(
            start__gte=midnight,
            start__lt=midnight + datetime.timedelta(days=1),
        )]
        start_times = [
            tz.localize(datetime.datetime.combine(self.date, time))
        for time in self.start_times]
        return Template(
            start_times=start_times,
            targets=self.targets,
            slot_duration=self.booking_duration,
            booked_slots=slots,
        )
