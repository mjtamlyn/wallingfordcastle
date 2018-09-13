import datetime
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from wallingford_castle.models import Archer


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')

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

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Session at %s' % self.start_time


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
        if self.member:
            return self.course.members_price
        return self.course.price
        # TODO: handle by session fees at some point


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


class CourseSignup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    student_name = models.CharField(max_length=255)
    student_date_of_birth = models.DateField()
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    gdpr_consent = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name


class Summer2018Signup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
