from django.db import models
from django.contrib.postgres.fields import ArrayField

from membership.models import Member


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    guests = ArrayField(models.CharField(max_length=255), blank=True, default=[])
    date = models.DateTimeField()
    duration = models.DurationField()

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
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return 'Member %s attending event %s' % (self.member_id, self.event_id)

    class Meta:
        unique_together = ['member', 'event']
