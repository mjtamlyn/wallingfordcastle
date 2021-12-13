import datetime
import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from events.models import Event
from wallingford_castle.models import Archer


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    coaches = models.ManyToManyField(Archer, blank=True)

    price = models.IntegerField(blank=True, null=True)
    members_price = models.IntegerField(blank=True, null=True)

    can_book_individual_sessions = models.BooleanField(default=False)
    price_per_session = models.IntegerField(blank=True, null=True)
    members_price_per_session = models.IntegerField(blank=True, null=True)

    open_for_bookings = models.BooleanField(default=False)
    open_to_members = models.BooleanField(default=False)
    open_to_non_members = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.DurationField(default=datetime.timedelta(minutes=90))
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)

    public_label = models.CharField(max_length=100, blank=True, default='')
    session_plan = models.TextField(blank=True, default='')
    session_notes = models.TextField(blank=True, default='')

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    @property
    def local_start_time(self):
        return settings.TZ.normalize(self.start_time)

    @property
    def end_time(self):
        return self.start_time + self.duration

    @property
    def local_end_time(self):
        return settings.TZ.normalize(self.end_time)

    @property
    def label(self):
        label = self.local_start_time.strftime('%d %b %Y, %-I:%M%p')
        if self.public_label:
            label += ' (%s)' % self.public_label
        return label

    def __str__(self):
        return 'Session at %s' % self.local_start_time


class Attendee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)
    member = models.BooleanField(default=True)
    group = models.CharField(max_length=30, blank=True, default='')
    contact_name = models.CharField(max_length=255, blank=True, default='')
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    communication_notes = models.TextField(blank=True, default='')
    gdpr_consent = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Attendee %s on course %s' % (self.archer, self.course)

    @property
    def fee(self):
        # Note: By session courses are marked as paid on the AttendeeSession.
        if self.member:
            return self.course.members_price
        return self.course.price


class AttendeeSession(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='session_set')
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    @property
    def fee(self):
        if self.attendee.member:
            return self.attendee.course.members_price_per_session
        return self.attendee.course.price_per_session

    def __str__(self):
        return 'Attendee %s attending session %s' % (self.attendee, self.session)


class Interest(models.Model):
    course_type = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=20, blank=True, default='')
    date_of_birth = models.DateField()
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    gdpr_consent = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)

    communication_notes = models.TextField(blank=True, default='')
    processed = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def convert_to_archer(self, user):
        today = datetime.date.today()
        age = relativedelta(today, self.date_of_birth).years
        archer, _ = Archer.objects.get_or_create(
            name=self.name,
            user=user,
            defaults={
                'date_of_birth': self.date_of_birth,
                'age': 'senior' if age >= 18 else 'junior',
                'contact_number': self.contact_number,
            }
        )
        return archer

    def book_trial(self, user, group, dates):
        from coaching.models import Trial

        archer = self.convert_to_archer(user)
        trial = Trial.objects.create(
            archer=archer,
            group=group,
            session_1=dates[0],
            session_2=dates[1],
            session_3=dates[2],
            session_4=dates[3],
            paid=False
        )
        return trial


class Summer2018Signup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    archer = models.ForeignKey(Archer, blank=True, null=True, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    student_name = models.CharField(max_length=255)
    student_date_of_birth = models.DateField()
    dates = ArrayField(models.DateField())
    group = models.CharField(max_length=30)
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    gdpr_consent = models.BooleanField(default=False)
    contact_consent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name
