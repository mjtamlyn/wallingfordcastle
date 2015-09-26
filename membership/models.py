from django.db import models

from wallingford_castle.models import AGE_CHOICES, MEMBERSHIP_CHOICES


class Member(models.Model):
    user = models.ForeignKey('auth.User', related_name='members')
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    agb_number = models.CharField(max_length=10, default='', blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    paid_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
