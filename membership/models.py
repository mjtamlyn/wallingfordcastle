from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.functional import cached_property

from wallingford_castle.models import MEMBERSHIP_CHOICES, Season


class MemberManager(models.Manager):
    def managed_by(self, user):
        members = (self.filter(archer__user=user) | self.filter(archer__managing_users=user)) & self.filter(active=True)
        return members.distinct()


LEVEL_CHOICES = (
    ('', 'Unknown'),
    ('performance', 'Performance'),
    ('development', 'Development'),
    ('leisure', 'Leisure'),
    ('novice', 'Novice'),
)


class Member(models.Model):
    archer = models.ForeignKey('wallingford_castle.Archer', on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    interest = models.ForeignKey(
        'wallingford_castle.MembershipInterest',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    coaching_subscription = models.BooleanField(default=False)
    coaching_individual = models.IntegerField(default=0)
    junior_training = models.IntegerField(default=0)

    active = models.BooleanField(default=True)
    agb_valid_until = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    def __str__(self):
        return self.archer.name

    def clean(self):
        if (self.coaching_subscription and self.coaching_individual):
            raise ValidationError('Please choose only one coaching subscription level')

    @property
    def plan(self):
        if self.archer.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        elif self.membership_type == 'minis':
            return 'minis'
        return 'concession'

    @property
    def prices(self):
        prices = [settings.STRIPE_PRICES[self.plan]]
        if self.archer.age == 'junior' and self.coaching_subscription:
            prices.append(settings.STRIPE_PRICES['coaching-junior'])
        if self.archer.age == 'senior' and self.coaching_subscription:
            prices.append(settings.STRIPE_PRICES['coaching-adult'])
        if self.junior_training:
            plan = settings.STRIPE_PRICES['coaching-junior-training']
            prices.append({
                'id': plan['id'],
                'quantity': self.junior_training,
                'price': plan['price'] * self.junior_training,
            })
        if self.coaching_individual:
            plan = settings.STRIPE_PRICES['coaching-individual']
            prices.append({
                'id': plan['id'],
                'quantity': self.coaching_individual,
                'price': plan['price'] * self.coaching_individual,
            })
        return prices

    @property
    def plan_cost(self):
        return sum(price['price'] for price in self.prices)

    def upcoming_bookings(self):
        today = timezone.now().date()
        return self.archer.bookedslot_set.filter(start__date__gte=today).order_by('start')

    @cached_property
    def coaching_groups(self):
        from coaching.models import TrainingGroup

        season = Season.objects.get_current()
        try:
            return self.archer.training_groups.filter(season=season).order_by('session_day')
        except TrainingGroup.DoesNotExist:
            return None

    @cached_property
    def upcoming_coaching_groups(self):
        from coaching.models import TrainingGroup

        season = Season.objects.get_upcoming()
        try:
            return self.archer.training_groups.filter(season=season).order_by('session_day')
        except TrainingGroup.DoesNotExist:
            return None

    @property
    def coaching_level(self):
        if self.coaching_groups and self.coaching_groups[0].level.first().name.startswith('Mini'):
            return 'Minis'
        if self.coaching_individual:
            return 'Private lessons'
        elif self.junior_training:
            return 'Junior Pro External'
        if self.coaching_subscription:
            if self.archer.age == 'junior':
                return 'Junior group'
            return 'Adult group'
        return 'Uncoached'
