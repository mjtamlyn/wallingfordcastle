import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone

from wallingford_castle.models import User


GENDER_CHOICES = (
    ('gent', 'Gent'),
    ('lady', 'Lady'),
)

BOWSTYLE_CHOICES = (
    ('recurve', 'Recurve'),
    ('compound', 'Compound'),
)


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField()

    # Prospectus information
    rounds = models.TextField()
    event_format = models.TextField()
    judges = models.TextField()
    awards = models.TextField()
    tournament_organiser = models.CharField(max_length=200)
    tournament_organiser_email = models.EmailField()
    dress = models.TextField()
    drug_testing = models.TextField()

    # Important information
    timing = models.TextField()
    venue_description = models.TextField()
    venue_google_search = models.CharField(max_length=200)
    refreshments = models.TextField()
    camping = models.TextField()

    # Entry information
    entry_information = models.TextField()
    entry_fee = models.IntegerField()
    entries_open = models.DateTimeField()
    entries_close = models.DateTimeField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tournaments:tournament-detail', kwargs={'tournament_slug': self.slug})

    @property
    def is_future(self):
        date = datetime.datetime.combine(self.date, datetime.datetime.min.time())
        date = date.replace(tzinfo=timezone.utc)
        return date > timezone.now()

    @property
    def entry_will_open(self):
        return timezone.now() < self.entries_close

    @property
    def entry_is_open(self):
        return self.entries_open < timezone.now() < self.entries_close

    @property
    def past(self):
        return timezone.now() >= self.date


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    agb_number = models.CharField('ArcheryGB number', max_length=50)
    club = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    bowstyle = models.CharField(max_length=50, choices=BOWSTYLE_CHOICES)
    notes = models.TextField(help_text='''
        Please include details of any accessibility requirements, other
        bowstyles, junior or masters age categories etc.
    ''', blank=True, default='')
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'entries'
