import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from records.classifications import CLASSIFICATION_CHOICES
from wallingford_castle.models import AGE_CHOICES

DAY_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class TrainingGroupType(models.Model):
    name = models.CharField(max_length=255)
    age_group = models.CharField(max_length=20, choices=AGE_CHOICES)
    trial_fee = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class TrainingGroup(models.Model):
    level = models.ManyToManyField(TrainingGroupType)
    season = models.ForeignKey('wallingford_castle.Season', on_delete=models.PROTECT)
    coaches = models.ManyToManyField('wallingford_castle.Archer', related_name='coached_groups')
    participants = models.ManyToManyField('wallingford_castle.Archer', related_name='training_groups')
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    session_day = models.SmallIntegerField(choices=DAY_CHOICES)
    session_start_time = models.TimeField()
    session_duration = models.DurationField(default=datetime.timedelta(minutes=90))
    number_of_targets = models.PositiveIntegerField(blank=True, null=True)
    target = models.PositiveIntegerField(default=1)
    b_range = models.BooleanField(default=False)
    venue = models.ForeignKey('venues.Venue', on_delete=models.PROTECT)

    @property
    def group_name(self):
        return '/'.join(map(str, self.level.all()))

    @property
    def slug(self):
        return '%s-%s' % (
            self.get_session_day_display().lower(),
            '-'.join(map(lambda s: str(s).replace(' ', '_').lower(), self.level.all())),
        )

    @property
    def time(self):
        return '%ss at %s' % (self.get_session_day_display(), self.session_start_time.strftime('%H:%M'))

    @property
    def session_end_time(self):
        today = timezone.now().date()
        possible_start = datetime.datetime.combine(today, self.session_start_time)
        possible_end = possible_start + self.session_duration
        return possible_end.time()

    @property
    def session_minutes(self):
        return int(self.session_duration.seconds / 60)

    def possible_dates(self, after=None):
        first_date = after or self.season.start_date
        while first_date.weekday() != self.session_day:
            first_date += datetime.timedelta(days=1)
        dates = [first_date]
        while dates[-1] <= self.season.end_date - datetime.timedelta(days=7):
            dates.append(dates[-1] + datetime.timedelta(days=7))
        return dates

    def next_session(self):
        today = timezone.now().date()
        return self.groupsession_set.filter_running().filter(
            start__date__gte=today,
        ).first()

    def additional_bookable_archers(self, user, already_booked=None):
        user_archers = set(m.archer for m in user.managed_members)
        current_archers = set(self.participants.all())
        if already_booked is not None:
            current_archers = current_archers & set(already_booked)

        levels = self.level.all()
        other_groups = TrainingGroup.objects.filter(level__in=levels, season_id=self.season_id)
        candidate_archers = set()
        for group in other_groups:
            candidate_archers |= set(group.participants.all())

        if already_booked is not None:
            candidate_archers -= set(already_booked)

        return sorted(user_archers & candidate_archers - current_archers, key=lambda a: a.name)

    def __str__(self):
        return '%s %s group (%s)' % (self.get_session_day_display(), self.group_name, self.season)


class GroupSessionQuerySet(models.QuerySet):
    def filter_running(self):
        return self.filter(cancelled_because='')


class GroupSession(models.Model):
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    start = models.DateTimeField()
    cancelled_because = models.TextField(blank=True, default='')
    booked_slot = models.OneToOneField('events.BookedSlot', blank=True, null=True, on_delete=models.SET_NULL)

    objects = models.Manager.from_queryset(GroupSessionQuerySet)()

    class Meta:
        unique_together = ['group', 'start']

    def __str__(self):
        return '%s session on %s' % (self.group, self.start)


class Absence(models.Model):
    session = models.ForeignKey(GroupSession, on_delete=models.CASCADE)
    archer = models.ForeignKey('wallingford_castle.Archer', on_delete=models.CASCADE)
    reason = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('session', 'archer')

    def __str__(self):
        return '%s absent from %s' % (self.archer, self.session)


class TrialQuerySet(models.QuerySet):
    def filter_ongoing(self):
        return self.filter(session_4__gte=timezone.now().date())

    def filter_completed(self):
        return self.filter(
            session_4__lt=timezone.now() + datetime.timedelta(days=5),
            archer__member__isnull=True,
        )


class Trial(models.Model):
    archer = models.ForeignKey('wallingford_castle.Archer', on_delete=models.CASCADE)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    session_1 = models.DateTimeField()
    session_2 = models.DateTimeField()
    session_3 = models.DateTimeField()
    session_4 = models.DateTimeField()
    paid = models.BooleanField(default=False)

    objects = models.Manager.from_queryset(TrialQuerySet)()

    def __str__(self):
        return '%s trial at %s' % (self.archer, self.group)

    @property
    def fee(self):
        return self.group.level.order_by('-trial_fee').first().trial_fee or 0


class CompetitiveTrack(models.Model):
    season = models.ForeignKey('wallingford_castle.Season', on_delete=models.PROTECT)
    number = models.IntegerField()
    name = models.CharField(max_length=100)

    @property
    def slug(self):
        return 'track-%s-%s' % (self.number, slugify(self.season.name))

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    event_format = models.CharField(max_length=100)
    track = models.ForeignKey(CompetitiveTrack, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=255)
    venue_post_code = models.CharField(max_length=20)
    age_groups = models.CharField(max_length=100)  # TODO? This could be improved to a multiple choice
    tournament_id = models.ForeignKey('tournaments.Tournament', on_delete=models.SET_NULL, blank=True, null=True)
    event_id = models.ForeignKey('events.Event', on_delete=models.SET_NULL, blank=True, null=True)
    club_trip = models.BooleanField(default=False)
    entry_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class ArcherSeason(models.Model):
    archer = models.ForeignKey('wallingford_castle.Archer', on_delete=models.CASCADE)
    season = models.ForeignKey('wallingford_castle.Season', on_delete=models.PROTECT)
    target_classification = models.CharField(max_length=3, choices=CLASSIFICATION_CHOICES)
    personalised_target_comments = models.TextField(blank=True, default='')
    tracks = models.ManyToManyField(CompetitiveTrack, through='ArcherTrack')
    events = models.ManyToManyField(Event, through='Registration')

    def __str__(self):
        return '%s in the %s season' % (self.archer, self.season)


class ArcherTrack(models.Model):
    track = models.ForeignKey(CompetitiveTrack, on_delete=models.CASCADE)
    archer_season = models.ForeignKey(ArcherSeason, on_delete=models.CASCADE)
    recommended_events_comments = models.TextField(blank=True, default='')

    def __str__(self):
        return '%s - %s track' % (self.archer_season, self.track)


class Registration(models.Model):
    STATUS_CHOICES = (
        ('definite', 'Yes, I am definitely attending'),
        ('booked', 'Yes, I am booked in'),
        ('maybe', 'I might be attending'),
        ('no', 'I will not be attending'),
    )
    TRANSPORT_CHOICES = (
        ('required', 'I can only attend if transport is offered'),
        ('interested', 'Transport for archer would be helpful but we could make our own way there'),
        ('plus-parent', 'Transport for archer and a parent would be helpful but we could make our own way there'),
        ('own-way', 'We will make our own way there'),
    )

    archer_season = models.ForeignKey(ArcherSeason, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    wants_transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)

    def __str__(self):
        return '%s registered for %s' % (self.archer_season.archer, self.event)
