from django.db import models
from django.utils import timezone

import stripe

from wallingford_castle.models import AGE_CHOICES, MEMBERSHIP_CHOICES


class MemberManager(models.Manager):
    def managed_by(self, user):
        return self.filter(archer__user=user) | self.filter(archer__managing_users=user)


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
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='', blank=True)
    interest = models.ForeignKey('wallingford_castle.MembershipInterest', blank=True, null=True, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    def __str__(self):
        return self.archer.name

    @property
    def plan(self):
        if self.membership_type == 'non-shooting':
            return 'non-shooting'
        if self.archer.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        return 'concession'

    @property
    def plan_cost(self):
        return {
            'adult': 15,
            'concession': 10,
            'non-shooting': 5,
        }[self.plan]
