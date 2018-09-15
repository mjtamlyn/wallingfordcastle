from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

from membership.models import Member
from wallingford_castle.models import Archer


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    guests = ArrayField(models.CharField(max_length=255), blank=True, default=list)
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
        return self.attendee_set.count() + len(self.guests)


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
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response_answers = HStoreField()

    def __str__(self):
        return 'Member %s booking in for event %s' % (self.member_id, self.event_id)

    class Meta:
        unique_together = ['member', 'event']

    @property
    def responses(self):
        return '\n'.join(['%s - %s' % (question, answer) for question, answer in self.response_answers.items()])
