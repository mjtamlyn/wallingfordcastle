from django.db import models

from wallingford_castle.models import User


GENDER_CHOICES = (
    ('gent', 'Gent'),
    ('lady', 'Lady'),
)

BOWSTYLE_CHOICES = (
    ('recurve', 'Recurve'),
    ('compound', 'Compound'),
)


class Entry(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    agb_number = models.CharField('ArcheryGB number', max_length=50)
    club = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    bowstyle = models.CharField(max_length=50, choices=BOWSTYLE_CHOICES)
    notes = models.TextField(help_text='''
        Please include details of any accessibility requirements, other
        bowstyles, junior or masters age categories etc.
    ''', blank=True, default='')
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
