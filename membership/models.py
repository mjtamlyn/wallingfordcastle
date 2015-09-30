from django.db import models
from django.utils import timezone

from wallingford_castle.models import AGE_CHOICES, MEMBERSHIP_CHOICES


class Member(models.Model):
    user = models.ForeignKey('wallingford_castle.User', related_name='members')
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    paid_until = models.DateField(blank=True, null=True)
    subscription_id = models.CharField(max_length=20, default='', blank=True, editable=False)
    interest = models.ForeignKey('wallingford_castle.MembershipInterest', blank=True, null=True)

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def plan(self):
        if self.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        return 'concession'

    @property
    def plan_cost(self):
        return 15 if self.plan == 'adult' else 10

    # TODO: Cancel subscription?
