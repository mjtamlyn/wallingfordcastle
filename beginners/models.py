import datetime

from django.db import models
from django.utils import timezone

from wallingford_castle.models import AGE_CHOICES, User


class BeginnersCourseManager(models.Manager):
    def current(self):
        now = timezone.now()
        return self.filter(
            beginnerscoursesession__start_time__gt=now,
        ).exclude(pk__in=self.upcoming().values_list('id', flat=True)).distinct()

    def upcoming(self):
        now = timezone.now()
        return self.exclude(beginnerscoursesession__start_time__lt=now).distinct()


class BeginnersCourse(models.Model):
    counter = models.PositiveIntegerField(verbose_name='Beginners course #', unique=True)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    objects = BeginnersCourseManager()

    def __str__(self):
        return 'Beginners course #%s' % self.counter

    class Meta:
        ordering = ('-counter',)


class BeginnersCourseSession(models.Model):
    course = models.ForeignKey(BeginnersCourse)
    start_time = models.DateTimeField()
    duration = models.DurationField(default=datetime.timedelta(minutes=90))

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Beginners course session at %s' % self.start_time

    def time_string(self):
        return '%s, %s to %s' % (
            self.start_time.strftime('%d %B %Y'),
            self.start_time.strftime('%H:%M'),
            (self.start_time + self.duration).strftime('%H:%M'),
        )


STATUS_WAITING = 'waiting'
STATUS_NOT_INTERESTED = 'not-interested'
STATUS_ON_COURSE = 'on-course'
STATUS_JOINED = 'joined'
STATUS_LEFT = 'left'
STATUS_CHOICES = (
    (STATUS_WAITING, 'Waiting for a course'),
    (STATUS_NOT_INTERESTED, 'No longer interested'),
    (STATUS_ON_COURSE, 'Allocated a course'),
    (STATUS_JOINED, 'Completed course and joined the club'),
    (STATUS_LEFT, 'Completed course but did not join'),
)


class Beginner(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=20, blank=True, default='')
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    experience = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')

    user = models.ForeignKey(User, blank=True, null=True)

    course = models.ForeignKey(BeginnersCourse, blank=True, null=True)
    paid = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=32, blank=True, default='')
    communication_notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_WAITING)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
