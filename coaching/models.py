from django.db import models
from django.utils import timezone

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
    session_day = models.SmallIntegerField(choices=DAY_CHOICES)
    session_start_time = models.TimeField()

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

    def __str__(self):
        return '%s group (%s)' % (self.group_name, self.season)


class TrialQuerySet(models.QuerySet):
    def filter_ongoing(self):
        return self.filter(session_4__gte=timezone.now().date())


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
