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
    coaching_conversion = models.BooleanField(default=False)
    coaching_performance = models.BooleanField(default=False)
    gym_supplement = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    def __str__(self):
        return self.archer.name

    def clean(self):
        if (self.coaching_subscription and self.coaching_conversion or
                self.coaching_subscription and self.coaching_performance or
                self.coaching_conversion and self.coaching_performance):
            raise ValidationError('Please choose only one coaching subscription level')

    @property
    def plan(self):
        if self.membership_type == 'non-shooting':
            return 'non-shooting'
        if self.archer.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        return 'concession'

    @property
    def prices(self):
        prices = [settings.STRIPE_PRICES[self.plan]]
        if self.archer.age == 'junior':
            if self.coaching_performance:
                prices.append(settings.STRIPE_PRICES['coaching-junior-performance'])
            elif self.coaching_conversion:
                prices.append(settings.STRIPE_PRICES['coaching-junior-conversion'])
            elif self.coaching_subscription:
                prices.append(settings.STRIPE_PRICES['coaching-junior'])
            if self.gym_supplement:
                prices.append(settings.STRIPE_PRICES['coaching-gym'])
        elif self.coaching_subscription:
            prices.append(settings.STRIPE_PRICES['coaching-adult'])
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
