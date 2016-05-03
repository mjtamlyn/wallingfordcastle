from django.db import models
from django.utils import timezone

import stripe

from wallingford_castle.models import AGE_CHOICES, MEMBERSHIP_CHOICES


class Member(models.Model):
    user = models.ForeignKey('wallingford_castle.User', related_name='members')
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    squad = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    address = models.TextField(default='')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    paid_until = models.DateField(blank=True, null=True)
    subscription_id = models.CharField(max_length=20, default='', blank=True, editable=False)
    interest = models.ForeignKey('wallingford_castle.MembershipInterest', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, default='')

    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def plan(self):
        if self.squad:
            return 'squad'
        if self.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        return 'concession'

    @property
    def plan_cost(self):
        return {
            'squad': 40,
            'adult': 15,
            'concession': 10,
        }[self.plan]

    def update_plan(self):
        if self.subscription_id:
            customer = stripe.Customer.retrieve(self.user.customer_id)
            subscription = customer.subscriptions.retrieve(self.subscription_id)
            subscription.plan = self.plan
            subscription.save()

    # TODO: Cancel subscription?
