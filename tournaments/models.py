import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils import timezone

from archery.bows import BOWSTYLE_CHOICES
from wallingford_castle.models import User

GENDER_CHOICES = (
    ('gent', 'Gent'),
    ('lady', 'Lady'),
)


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField()

    # Prospectus information
    rounds = models.ManyToManyField('archery.Round')
    has_wrs = models.BooleanField(default=True)
    bowstyles = ArrayField(models.CharField(max_length=30, choices=BOWSTYLE_CHOICES))
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
    camping = models.TextField(blank=True, default='')

    # Entry information
    entry_information = models.TextField()
    entry_fee = models.IntegerField()
    entries_open = models.DateTimeField()
    entries_close = models.DateTimeField()
    waiting_list_enabled = models.BooleanField(default=False)

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
        return timezone.now() < self.entries_open

    @property
    def entry_is_open(self):
        return self.entries_open < timezone.now() < self.entries_close


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    agb_number = models.CharField('ArcheryGB number', max_length=50)
    club = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True, help_text='Required for junior archers.')
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    bowstyle = models.CharField(max_length=50, choices=BOWSTYLE_CHOICES)
    round = models.ForeignKey('archery.Round', blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(help_text='''
        Please include details of any accessibility requirements, session and
        target face preferences, other bowstyles, junior or masters age
        categories etc.
    ''', blank=True, default='')
    drugs_consent = models.BooleanField('I consent to drugs testing as required under WRS rules.', default=False)
    gdpr_consent = models.BooleanField(
        verbose_name=(
            'I consent that some of the information here provided will be shared '
            'with tournament organisers, scoring systems, other competitors and '
            'ArcheryGB. I also consent that I may be contacted with further details '
            'of the event via email.'
        ),
        default=False,
    )
    future_event_consent = models.BooleanField(
        verbose_name='Please contact me about future competitions at Wallingford Castle Archers',
        default=False,
    )
    paid = models.BooleanField(default=False)
    waiting_list = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'entries'
