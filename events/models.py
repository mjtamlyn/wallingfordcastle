import datetime

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models
from django.utils.functional import cached_property

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
    b_range = models.BooleanField(default=False)
    venue = models.ForeignKey('venues.Venue', blank=True, null=True, on_delete=models.SET_NULL)
    face = models.IntegerField(choices=((1, 'A'), (2, 'B')), blank=True, null=True, default=None)
    distance = models.CharField(max_length=100, default='', blank=True)
    archers = models.ManyToManyField(Archer, blank=True)

    # Group fields
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=100, default='', blank=True)
    number_of_targets = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('start', 'target', 'face')

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
            venue=self.venue.slug if self.venue else None,
            b_range=self.b_range,
            face=self.get_face_display(),
            number_of_targets=self.number_of_targets,
            booked=True,
            details=self,
            is_group=self.is_group,
            group_name=self.group_name,
        )

    @cached_property
    def booking_template(self):
        return BookingTemplate.objects.get(date=self.start.date())


class BookingTemplate(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200, blank=True, default='')
    venue = models.ForeignKey('venues.Venue', blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, default='')
    start_times = ArrayField(models.TimeField())
    targets = models.PositiveIntegerField()
    b_targets = models.PositiveIntegerField(blank=True, null=True, help_text='Enables a split range')
    booking_duration = models.DurationField()
    multiple_archers_permitted = models.BooleanField(default=True)
    ab_faces = models.BooleanField(default=False)
    distance_required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('date', 'venue')

    def __str__(self):
        return 'Booking template for %s' % self.date

    @cached_property
    def template(self):
        slots = [slot.slot for slot in self.slots]
        start_times = [
            datetime.datetime.combine(self.date, time, tzinfo=settings.TZ)
            for time in self.start_times
        ]
        return Template(
            start_times=start_times,
            venue=self.venue.slug if self.venue else None,
            targets=self.targets,
            b_targets=self.b_targets,
            slot_duration=self.booking_duration,
            booked_slots=slots,
            ab_faces=self.ab_faces,
        )

    @property
    def slots(self):
        midnight = datetime.datetime.combine(self.date, datetime.time(0), tzinfo=settings.TZ)
        return BookedSlot.objects.filter(
            start__gte=midnight,
            start__lt=midnight + datetime.timedelta(days=1),
            venue=self.venue,
        )

    def update_from_coaching(self):
        from coaching.models import GroupSession

        # Delete pre-existing groups and recreate them
        self.slots.filter(is_group=True).delete()

        # Training groups
        sessions = GroupSession.objects.filter_running().filter(start__date=self.date).select_related('group')
        for session in sessions:
            group = session.group
            archers = list(group.participants.all())
            trials = group.trial_set.all()
            for trial in trials:
                if session.start in [trial.session_1, trial.session_2, trial.session_3, trial.session_4]:
                    archers.append(trial.archer)
            number_of_targets = len(archers) / 2 + (len(archers) % 2 > 0)
            if self.targets < 5 or group.level.first().age_group == 'junior':
                number_of_targets = self.targets
            new_slot = BookedSlot.objects.create(
                start=session.start,
                duration=group.session_duration,
                target=1,
                b_range=group.b_range,
                face=1 if self.ab_faces else None,
                is_group=True,
                group_name='%s (%ss)' % (group.group_name, group.get_session_day_display()),
                number_of_targets=number_of_targets,
            )
            new_slot.archers.set(archers)
            session.booked_slot = new_slot
            session.save()

    def create_next(self, date=None):
        if date is None:
            date = self.date + datetime.timedelta(days=7)
        new = BookingTemplate.objects.create(
            date=date,
            title=self.title,
            notes=self.notes,
            venue=self.venue,
            start_times=self.start_times,
            targets=self.targets,
            b_targets=self.b_targets,
            booking_duration=self.booking_duration,
            ab_faces=self.ab_faces,
            multiple_archers_permitted=self.multiple_archers_permitted,
            distance_required=self.distance_required,
        )
        return new
