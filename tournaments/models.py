import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe

from archery.bows import BOWSTYLE_CHOICES
from wallingford_castle.models import User

GENDER_CHOICES = (
    ('gent', 'Men'),
    ('lady', 'Women'),
)


class TournamentDetailsBase(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField()

    # Prospectus information
    rounds = models.ManyToManyField('archery.Round')
    has_wrs = models.BooleanField(default=True)
    has_ukrs = models.BooleanField(default=False)
    indoors = models.BooleanField(default=False, help_text='Displays indoor image.')
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def labelled_rounds(self):
        labels = []
        for shot_round in self.rounds.order_by('id'):  # TODO: Better ordering for rounds
            if self.has_wrs and shot_round.can_be_wrs:
                labels.append('WRS %s' % shot_round)
            elif self.has_wrs and not shot_round.can_be_wrs:
                labels.append('UKRS %s' % shot_round)
            elif self.has_ukrs:
                labels.append('UKRS %s' % shot_round)
            else:
                labels.append(str(shot_round))
        return labels

    @property
    def is_future(self):
        date = datetime.datetime.combine(self.date, datetime.datetime.min.time())
        date = date.replace(tzinfo=datetime.timezone.utc)
        return date > timezone.now()

    @property
    def entry_is_open(self):
        return self.entries_open < timezone.now() < self.entries_close


class Tournament(TournamentDetailsBase):
    tamlynscore_id = models.SlugField(blank=True, default='')
    full_results_document = models.URLField(blank=True, default='')
    series = models.ForeignKey('tournaments.Series', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('tournaments:tournament-detail', kwargs={'tournament_slug': self.slug})

    @property
    def entry_will_open(self):
        return timezone.now() < self.entries_open

    def entry_summary(self):
        if len(self.rounds.all()) == 1:
            return None
        by_round = []
        for r in self.rounds.all():
            count = self.entry_set.filter(round=r).count()
            by_round.append((r, count))
        return mark_safe('<br />'.join('%s: %s' % (r, c) for (r, c) in by_round))


class Series(TournamentDetailsBase):
    is_series = True

    def get_absolute_url(self):
        return reverse('tournaments:series-detail', kwargs={'series_slug': self.slug})

    class Meta:
        verbose_name_plural = 'series'

    def ordered_tournaments(self):
        return self.tournament_set.order_by('date')


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True, null=True)
    series_entry = models.BooleanField(default=False)
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
