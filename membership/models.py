import datetime

from django.db import models
from django.utils import timezone

import stripe
from dateutil.relativedelta import relativedelta

from wallingford_castle.models import AGE_CHOICES, MEMBERSHIP_CHOICES


LEVEL_CHOICES = (
    ('', 'Unknown'),
    ('performance', 'Performance'),
    ('development', 'Development'),
    ('leisure', 'Leisure'),
    ('novice', 'Novice'),
)


class Member(models.Model):
    user = models.ForeignKey('wallingford_castle.User', related_name='members', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    address = models.TextField(default='')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='', blank=True)
    paid_until = models.DateField(blank=True, null=True)
    subscription_id = models.CharField(max_length=20, default='', blank=True, editable=False)
    interest = models.ForeignKey('wallingford_castle.MembershipInterest', blank=True, null=True, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=True, default='')

    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def plan(self):
        if self.membership_type == 'non-shooting':
            return 'non-shooting'
        if self.age == 'senior' and self.membership_type == 'full':
            return 'adult'
        return 'concession'

    @property
    def plan_cost(self):
        return {
            'adult': 15,
            'concession': 10,
            'non-shooting': 5,
        }[self.plan]

    @property
    def age_group(self):
        if not self.date_of_birth:
            return None
        today = datetime.date.today()
        years = relativedelta(today, self.date_of_birth).years
        if years >= 25:
            return 'Senior'
        if years < 12:
            group = 'U12'
        elif years < 14:
            group = 'U14'
        elif years < 16:
            group = 'U16'
        elif years < 18:
            group = 'U18'
        else:
            group = 'Senior (U25)'
        this_years_birthday = self.date_of_birth.replace(year=today.year)
        days_to_birthday = (this_years_birthday - today).days
        if days_to_birthday < 0:
            this_years_birthday += relativedelta(years=1)
            days_to_birthday = (this_years_birthday - today).days
        if days_to_birthday < 90 and years % 2:
            group += ' (Moving up on %s)' % this_years_birthday.strftime('%d/%m/%Y')
        return group

    def update_plan(self):
        if self.subscription_id:
            customer = stripe.Customer.retrieve(self.user.customer_id)
            subscription = customer.subscriptions.retrieve(self.subscription_id)
            subscription.plan = self.plan
            subscription.save()

    # TODO: Cancel subscription?
